from psycopg2 import Error
from dao import bd


class Medico:
    def __init__(self, id_medico=None, nome=None, id_especialidade=None):
        self.id_medico = id_medico
        self.nome = nome
        self.id_especialidade = id_especialidade
        self.erro = None

    def salvar(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    INSERT INTO Medicos (Nome) VALUES (%s) RETURNING ID;
                    """, (self.nome,))
                    self.id_medico = cursor.fetchone()[0]

                    if self.id_especialidade:
                        cursor.execute("""
                        INSERT INTO EspecialidadeMedico (ID_Medico, ID_Especialidade) VALUES (%s, %s);
                        """, (self.id_medico, self.id_especialidade))

                    conexao.commit()
                    return True
        except Error as e:
            self.erro = f"Erro ao salvar médico: {str(e)}"
            conexao.rollback()
            return False

    def listar_especialidades(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            ID, Descr
                        FROM 
                            Especialidades 
                        ORDER BY
                            ID;
                    """)
                    resultados = cursor.fetchall()
            if resultados:
                return resultados
            else:
                self.erro = f"\nErro."
                return False
        except Error:
            self.erro = Error
            return False

    def carregar_dados(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT Nome FROM Medicos WHERE ID = %s;
                    """, (self.id_medico,))
                    dados = cursor.fetchone()
            if dados:
                self.nome = dados[0]
                return True
            else:
                self.erro = f"Medico ID {self.id_medico} não encontrado."
                return False
        except Error as e:
            self.erro = f"Erro ao carregar dados do médico: {str(e)}"
            return False

    def atualizar(self, novo_nome=None, nova_especialidade=None):
        self.nome = novo_nome or self.nome
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    UPDATE Medicos SET Nome = %s WHERE ID = %s;
                    """, (self.nome, self.id_medico))

                    if nova_especialidade:
                        cursor.execute("""
                        DELETE FROM EspecialidadeMedico WHERE ID_Medico = %s;
                        """, (self.id_medico,))
                        cursor.execute("""
                        INSERT INTO EspecialidadeMedico (ID_Medico, ID_Especialidade) VALUES (%s, %s);
                        """, (self.id_medico, nova_especialidade))

                    conexao.commit()
                    return True
        except Error as e:
            self.erro = f"Erro ao atualizar médico: {str(e)}"
            conexao.rollback()
            return False

    def listar_todos(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        m.ID, 
                        m.Nome, 
                        COALESCE(e.Descr, 'Nenhuma') as Especialidade
                    FROM 
                        Medicos m
                    LEFT JOIN 
                        EspecialidadeMedico em ON m.ID = em.ID_Medico
                    LEFT JOIN 
                        Especialidades e ON em.ID_Especialidade = e.ID
                    ORDER BY 
                        m.ID;
                    """)
                    medicos = cursor.fetchall()
            if medicos:
                return medicos
            else:
                self.erro = "Nenhum médico encontrado."
                return False
        except Error as e:
            self.erro = f"Erro ao listar médicos: {str(e)}"
            return False

    def excluir(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    DELETE FROM EspecialidadeMedico WHERE ID_Medico = %s;
                    """, (self.id_medico,))
                    cursor.execute("""
                    DELETE FROM Medicos WHERE ID = %s;
                    """, (self.id_medico,))
                    conexao.commit()
                    return True
        except Error as e:
            self.erro = f"Erro ao excluir médico: {str(e)}"
            conexao.rollback()
            return False
