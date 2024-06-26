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
                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_valor_servicos_por_sexo_tipo AS
                    SELECT 
                        p.Sexo,
                        ts.Tipo,
                        SUM(t.Valor) AS Valor_por_Tipo_de_Servico
                    FROM 
                        Servico s
                    JOIN 
                        Atendimento a ON s.ID_atend = a.ID_atend
                    JOIN 
                        Paciente p ON a.ID_paciente = p.ID_paciente
                    JOIN 
                        TUSS t ON s.ID_tuss = t.Cod_TUSS
                    JOIN 
                        TiposServicos ts ON t.ID_TiposServicos = ts.ID
                    GROUP BY 
                        p.Sexo, ts.Tipo;
                    """)

                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_valor_servicos_por_tipo_sexo AS
                    SELECT 
                        p.Sexo,
                        ts.Tipo,
                        SUM(t.Valor) AS Valor_por_Tipo_de_Servico
                    FROM 
                        Servico s
                    JOIN 
                        Atendimento a ON s.ID_atend = a.ID_atend
                    JOIN 
                        Paciente p ON a.ID_paciente = p.ID_paciente
                    JOIN 
                        TUSS t ON s.ID_tuss = t.Cod_TUSS
                    JOIN 
                        TiposServicos ts ON t.ID_TiposServicos = ts.ID
                    WHERE 
                        ts.Tipo = %s
                    GROUP BY 
                        p.Sexo, ts.Tipo;
                    """)

                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_valor_servicos_por_medico_tipo AS
                    SELECT 
                        m.ID,
                        m.Nome,
                        ts.Tipo,
                        SUM(t.Valor) AS Valor_por_Tipo_de_Servico
                    FROM 
                        Servico s
                    JOIN 
                        Medicos m ON s.Medicos_ID = m.ID
                    JOIN 
                        TUSS t ON s.ID_tuss = t.Cod_TUSS
                    JOIN 
                        TiposServicos ts ON t.ID_TiposServicos = ts.ID
                    GROUP BY 
                        m.ID, m.Nome, ts.Tipo;
                    """)

                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_valor_servicos_por_medico_tipo_especifico AS
                    SELECT 
                        m.ID,
                        m.Nome,
                        ts.Tipo,
                        SUM(t.Valor) AS Valor_por_Tipo_de_Servico
                    FROM 
                        Servico s
                    JOIN 
                        Medicos m ON s.Medicos_ID = m.ID
                    JOIN 
                        TUSS t ON s.ID_tuss = t.Cod_TUSS
                    JOIN 
                        TiposServicos ts ON t.ID_TiposServicos = ts.ID
                    WHERE 
                        m.Nome = %s
                    GROUP BY 
                        m.ID, m.Nome, ts.Tipo;
                    """)

                    cursor.execute("""
                    CREATE OR REPLACE VIEW vw_valor_servicos_por_atendimento AS
                    SELECT 
                        a.ID_atend,
                        SUM(t.Valor) AS Valor_Total_Servicos
                    FROM 
                        Servico s
                    JOIN 
                        Atendimento a ON s.ID_atend = a.ID_atend
                    JOIN 
                        TUSS t ON s.ID_tuss = t.Cod_TUSS
                    GROUP BY 
                        a.ID_atend;
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
