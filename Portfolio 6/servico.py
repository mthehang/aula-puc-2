from datetime import datetime
from dao import bd
from psycopg2 import Error


class Servico:
    def __init__(self, id_atend_serv=None, id_atend=None, id_tuss=None, medicos_id=None,
                 data_serv=datetime.now().strftime('%Y-%m-%d %H:%M')):
        self.id_atend_serv = id_atend_serv
        self.id_atend = id_atend
        self.id_tuss = id_tuss
        self.medicos_id = medicos_id
        self.data_serv = data_serv
        self.erro = None

    def salvar(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            ID_atend
                        FROM 
                            Atendimento 
                        WHERE 
                            ID_atend = %s;
                    """, (self.id_atend,))
                    if cursor.fetchone() is None:
                        self.erro = f"\nID de atendimento {self.id_atend} não existe."
                        return False

                    cursor.execute("""
                        SELECT
                            Cod_TUSS
                        FROM
                            TUSS
                        WHERE
                            Cod_TUSS = %s;
                    """, (self.id_tuss,))
                    if cursor.fetchone() is None:
                        self.erro = "\nCódigo TUSS não é válido"
                        return False

                    cursor.execute("""
                        SELECT
                            ID
                        FROM
                            Medicos
                        WHERE
                            ID = %s;
                    """, (self.medicos_id,))
                    if cursor.fetchone() is None:
                        self.erro = "\nID do médico não é válido"
                        return False

                    cursor.execute("""
                    SET 
                        datestyle = 'ISO, DMY';
                    """)
                    cursor.execute("""
                        INSERT INTO Servico (
                            id_atend, 
                            id_tuss, 
                            medicos_id,
                            data_serv
                        ) VALUES (%s, %s, %s, %s)
                        RETURNING ID_atend_serv;
                    """, (self.id_atend, self.id_tuss, self.medicos_id, self.data_serv))
                    self.id_atend_serv = cursor.fetchone()[0]

                    conexao.commit()
                    return True
        except Error as e:
            self.erro = f"Erro ao salvar serviço: {str(e)}"
            conexao.rollback()
            return False

    def listar_todos(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        ID_atend_serv,
                        ID_atend, 
                        ID_tuss, 
                        Medicos_ID,
                        to_char(Data_serv, 'DD/MM/YYYY HH24:MI')
                    FROM 
                        Servico
                    ORDER BY 
                        ID_atend_serv;
                    """)
                    servicos = cursor.fetchall()
            if servicos:
                return servicos
            else:
                self.erro = f"\nNenhum serviço encontrado."
                return False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def carregar_dados(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        ID_atend,
                        ID_TUSS,
                        Medicos_ID,
                        to_char(Data_serv, 'DD/MM/YYYY HH24:MI')
                    FROM 
                        Servico
                    WHERE 
                        ID_atend_serv = %s;
                    """, (self.id_atend_serv,))
                    dados = cursor.fetchone()
            if dados:
                self.id_atend, self.id_tuss, self.medicos_id, self.data_serv = dados
                return True
            else:
                self.erro = f"\nServiço ID {self.id_atend_serv} não encontrado."
                return False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def atualizar(self, novo_id_atend, novo_id_tuss, novo_medicos_id):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    novo_id_atend = int(novo_id_atend) if novo_id_atend.isdigit() else self.id_atend
                    novo_id_tuss = int(novo_id_tuss) if novo_id_tuss.isdigit() else self.id_tuss
                    novo_medicos_id = int(novo_medicos_id) if novo_medicos_id.isdigit() else self.medicos_id

                    cursor.execute("""
                    UPDATE Servico
                    SET ID_atend = %s, ID_tuss = %s, Medicos_ID = %s
                    WHERE ID_atend_serv = %s;
                    """, (novo_id_atend, novo_id_tuss, novo_medicos_id, self.id_atend_serv))
                    conexao.commit()
                    return True
        except Error as e:
            self.erro = str(e)
            conexao.rollback()
            return False

    def servicos_id_tuss(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            pac.Nome, 
                            to_char(atend.data_atend, 'DD/MM/YYYY HH24:MI'), 
                            SUM(tuss.Valor) AS Valor_Total
                        FROM 
                            Servico serv
                        JOIN 
                            Atendimento atend ON serv.id_atend = atend.ID_atend
                        JOIN 
                            Paciente pac ON atend.ID_paciente = pac.ID_paciente
                        JOIN 
                            TUSS tuss ON serv.id_tuss = tuss.Cod_TUSS
                        WHERE 
                            tuss.Cod_TUSS = %s
                        GROUP BY 
                            pac.Nome, 
                            atend.Data_atend;
                        """, (self.id_tuss,))
                    results = cursor.fetchall()
                    self.erro = "Erro ao pesquisar serviços prestados."
                    return results if results else False
        except Error as e:
            self.erro = "Erro: ", str(e)
            return False

    def servico_data(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            tuss.Cod_TUSS, 
                            pac.Sexo, 
                            COUNT(serv.ID_atend) AS Quantidade,
                            SUM(tuss.Valor) AS Valor_Total
                        FROM 
                            Servico serv
                        JOIN 
                            Atendimento atend ON serv.ID_atend = atend.ID_atend
                        JOIN 
                            Paciente pac ON atend.ID_paciente = pac.ID_paciente
                        JOIN 
                            TUSS tuss ON serv.ID_tuss = tuss.Cod_TUSS
                        WHERE 
                            serv.Data_serv::Date = %s
                        GROUP BY 
                            tuss.Cod_TUSS, pac.Sexo;
                    """, (self.data_serv,))
                    results = cursor.fetchall()
                    return results if results else False
        except Error as e:
            self.erro = f"Erro: {str(e)}"
            return False

    def excluir(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT 1 FROM Servico WHERE ID_atend_serv = %s;
                    """, (self.id_atend_serv,))
                    if cursor.fetchone() is None:
                        self.erro = f"Serviço com ID {self.id_atend_serv} não encontrado."
                        return False

                    cursor.execute("""
                        DELETE FROM Servico
                        WHERE ID_atend_serv = %s;
                    """, (self.id_atend_serv,))
                    conexao.commit()
                    return True
        except Error as e:
            self.erro = f"Erro ao excluir serviço: {str(e)}"
            return False

    def servicos_fora_especialidade(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
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
                    resultados = cursor.fetchall()
                    return resultados if resultados else False
        except Error as e:
            self.erro = f"Erro ao acessar dados do banco: {str(e)}"
            return False

    def quantidade_servicos_por_tipo(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
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
                    resultados = cursor.fetchall()
                    return resultados if resultados else False
        except Error as e:
            self.erro = f"Erro ao acessar dados do banco: {str(e)}"
            return False

    def servico_mais_uma_vez(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
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
                    resultados = cursor.fetchall()
                    return resultados if resultados else False
        except Error as e:
            self.erro = f"Erro ao acessar dados do banco: {str(e)}"
            return False

    def servicos_incompativeis_sexo(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
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
                    resultados = cursor.fetchall()
                    return resultados if resultados else False
        except Error as e:
            self.erro = f"Erro ao acessar dados do banco: {str(e)}"
            return False

    def servicos_fora_especialidade_medico(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
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
                    resultados = cursor.fetchall()
                    return resultados if resultados else False
        except Error as e:
            self.erro = f"Erro ao acessar dados do banco: {str(e)}"
            return False
