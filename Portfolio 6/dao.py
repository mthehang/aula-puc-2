import psycopg2
from psycopg2 import Error


class BancoDeDados:
    def __init__(self):
        self.login_db = {
            "host": "aws-0-sa-east-1.pooler.supabase.com",
            "database": "postgres",
            "user": "postgres.kpimaeplwogdjuqoxifx",
            "password": "pucsp@2024*"
        }

    def obter_conexao(self):
        try:
            return psycopg2.connect(**self.login_db)
        except psycopg2.OperationalError as e:
            print("Não foi possível conectar ao banco de dados:", e)
            return None

    def criar_tabelas(self):
        try:
            with self.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Paciente (
                        ID_paciente SERIAL PRIMARY KEY,
                        RG VARCHAR(20),
                        Nome VARCHAR(100),
                        Sexo VARCHAR(1),
                        Data_nasc DATE,
                        Peso INT,
                        Altura FLOAT
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Medicos (
                        ID SERIAL PRIMARY KEY,
                        Nome VARCHAR(45)
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TiposServicos (
                        ID SERIAL PRIMARY KEY,
                        Tipo VARCHAR(45)
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Atendimento (
                        ID_atend SERIAL PRIMARY KEY,
                        ID_paciente INT REFERENCES Paciente(ID_paciente) ON DELETE RESTRICT,
                        Data_atend TIMESTAMP,
                        CID_10 VARCHAR(10),
                        Cod_Manchester VARCHAR(8)
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS CID10 (
                        CAT VARCHAR(10) PRIMARY KEY,
                        DESCR VARCHAR(255)
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS TUSS (
                        Cod_TUSS VARCHAR(8) PRIMARY KEY,
                        Descr VARCHAR(255),
                        Valor FLOAT,
                        ID_TiposServicos INT REFERENCES TiposServicos(ID)
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Servico (
                        ID_atend_serv SERIAL PRIMARY KEY,
                        ID_atend INT REFERENCES Atendimento(ID_atend) ON DELETE RESTRICT,
                        ID_tuss VARCHAR(8) REFERENCES TUSS(Cod_TUSS),
                        Medicos_ID INT REFERENCES Medicos(ID),
                        Data_serv TIMESTAMP
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Restricoes (
                        COD_TUSS VARCHAR(8) REFERENCES TUSS(Cod_TUSS),
                        QtdPeriodo INT,
                        PeriodoMeses INT,
                        IdadeMin INT,
                        IdadeMax INT,
                        Sexo VARCHAR(1)
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Especialidades (
                        ID SERIAL PRIMARY KEY,
                        Descr VARCHAR(45)
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EspecialidadeTUSS (
                        Cod_Tuss VARCHAR(8) REFERENCES TUSS(Cod_Tuss),
                        ID_Especialidade INT REFERENCES Especialidades(ID)
                    );""")

                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS EspecialidadeMedico (
                        ID_Medico INT REFERENCES Medicos(ID),
                        ID_Especialidade INT REFERENCES Especialidades(ID)
                    );""")

                    conexao.commit()
                    print("Tabelas criadas com sucesso.")

        except Error as e:
            print("Não foi possível criar as tabelas: ", e)

    def alterar_tabelas(self):
        try:
            with self.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                            ALTER TABLE Atendimento 
                            ADD COLUMN IF NOT EXISTS Cod_Manchester VARCHAR(8);
                        """)

                    cursor.execute("""
                    ALTER TABLE
                        TUSS 
                    ADD COLUMN 
                        IF NOT EXISTS ID_TiposServicos INT REFERENCES TiposServicos(ID)
                    ;""")

                    cursor.execute("""
                    ALTER TABLE
                        Servico 
                    ADD COLUMN 
                        IF NOT EXISTS Medicos_ID INT REFERENCES Medicos(ID)
                    ;""")
                    conexao.commit()

                    print("Coluna adicionada com sucesso.")

        except Error as e:
            print("Não foi possível alterar as tabelas: ", e)

    def criar_views_compliance(self):
        try:
            with self.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    # View para Serviços fora da relação de Especialidades X Serviços
                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_servicos_fora_especialidade AS
                    SELECT 
                        s.ID_atend_serv, 
                        s.ID_atend, 
                        s.ID_tuss, 
                        s.Data_serv,
                        e.Descr AS Especialidade
                    FROM 
                        Servico s
                    LEFT JOIN 
                        TUSS t ON s.ID_tuss = t.Cod_TUSS
                    LEFT JOIN 
                        EspecialidadeTUSS et ON t.Cod_TUSS = et.Cod_Tuss
                    LEFT JOIN 
                        Especialidades e ON et.ID_Especialidade = e.ID
                    WHERE 
                        et.ID_Especialidade IS NULL;
                    """)

                    # View para Quantidade de serviços prestados por tipo de serviço
                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_quantidade_servicos_por_tipo AS
                    SELECT 
                        ts.Tipo, 
                        COUNT(s.ID_atend_serv) AS Quantidade
                    FROM 
                        TiposServicos ts
                    LEFT JOIN 
                        TUSS t ON ts.ID = t.ID_TiposServicos
                    LEFT JOIN 
                        Servico s ON t.Cod_TUSS = s.ID_tuss
                    GROUP BY 
                        ts.Tipo;
                    """)

                    # View para Pacientes que utilizaram serviço mais de uma vez
                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_pacientes_servico_mais_de_uma_vez AS
                    SELECT 
                        p.Nome,
                        p.ID_paciente,
                        t.Descr,
                        COUNT(s.ID_atend_serv) AS Quantidade
                    FROM 
                        Servico s
                    JOIN 
                        Atendimento a ON s.ID_atend = a.ID_atend
                    JOIN 
                        Paciente p ON a.ID_paciente = p.ID_paciente
                    JOIN 
                        TUSS t ON s.ID_tuss = t.Cod_TUSS
                    JOIN 
                        Restricoes r ON t.Cod_TUSS = r.COD_TUSS
                    WHERE 
                        r.QtdPeriodo = 1
                    GROUP BY 
                        p.Nome, p.ID_paciente, t.Descr
                    HAVING 
                        COUNT(s.ID_atend_serv) > 1;
                    """)

                    # View para Serviços incompatíveis com o sexo do paciente
                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_servicos_incompativeis_sexo AS
                    SELECT 
                        s.ID_atend_serv, 
                        s.ID_atend, 
                        s.ID_tuss, 
                        s.Data_serv,
                        p.Nome,
                        p.Sexo,
                        t.Descr
                    FROM 
                        Servico s
                    JOIN 
                        Atendimento a ON s.ID_atend = a.ID_atend
                    JOIN 
                        Paciente p ON a.ID_paciente = p.ID_paciente
                    JOIN 
                        TUSS t ON s.ID_tuss = t.Cod_TUSS
                    JOIN 
                        Restricoes r ON t.Cod_TUSS = r.COD_TUSS
                    WHERE 
                        p.Sexo != r.Sexo AND r.Sexo IS NOT NULL;
                    """)

                    # View para Serviços solicitados por médicos fora da especialidade
                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_servicos_fora_especialidade_medico AS
                    SELECT 
                        s.ID_atend_serv,
                        s.ID_atend,
                        s.ID_tuss,
                        to_char(s.Data_serv, 'DD/MM/YYYY HH24:MI'),
                        m.Nome,
                        e.Descr
                    FROM 
                        Servico s
                    JOIN 
                        Medicos m ON s.Medicos_ID = m.ID
                    LEFT JOIN 
                        EspecialidadeMedico em ON m.ID = em.ID_Medico
                    LEFT JOIN 
                        Especialidades e ON em.ID_Especialidade = e.ID
                    LEFT JOIN 
                        EspecialidadeTUSS et ON s.ID_tuss = et.Cod_Tuss
                    WHERE 
                        et.ID_Especialidade IS NULL OR et.ID_Especialidade != e.ID;
                    """)

                    conexao.commit()
                    print("Views criadas com sucesso.")

        except Error as e:
            print("Erro ao criar views: ", e)


bd = BancoDeDados()

if __name__ == '__main__':
    bd.criar_tabelas()
    bd.alterar_tabelas()
    bd.criar_views_compliance()
