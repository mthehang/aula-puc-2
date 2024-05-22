from datetime import datetime
from psycopg2 import Error
from dao import bd


class Atendimento:
    def __init__(self, id_atend=None, id_paciente=None, cid_10=None,
                 cod_manchester=None, data_atend=datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        self.id_atend = id_atend
        self.id_paciente = id_paciente
        self.data_atend = data_atend
        self.cid_10 = cid_10
        self.cod_manchester = cod_manchester
        self.erro = None

    def salvar(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""SELECT CAT FROM CID10 WHERE CAT = %s;""", (self.cid_10,))
                    if cursor.fetchone() is None:
                        self.erro = f"\nCID-10 {self.cid_10} inválido."
                        return False

                    cursor.execute("""SELECT 1 FROM Paciente WHERE ID_paciente = %s;""", (self.id_paciente,))
                    if cursor.fetchone() is None:
                        self.erro = f"\nID do paciente {self.id_paciente} não encontrado."
                        return False

                    cursor.execute("""INSERT INTO Atendimento (ID_paciente, Data_atend, CID_10)
                    VALUES (%s, %s, %s) RETURNING ID_atend;""",
                                   (self.id_paciente, self.data_atend, self.cid_10))
                    self.id_atend = cursor.fetchone()[0]
                    conexao.commit()
            return True
        except Error as e:
            self.erro = f"\n{str(e)}"
            conexao.rollback()
            return False

    def listar_data(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        """SELECT ID_atend, ID_paciente, Data_atend, CID_10 FROM Atendimento 
                        WHERE DATE(Data_atend) = %s ORDER BY ID_atend;""",
                        (self.data_atend,))
                    atendimentos = cursor.fetchall()
            if atendimentos:
                return True
            else:
                self.erro = f"\nNenhum atendimento encontrado para {self.data_atend}."
                return False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def listar_todos(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        """SELECT ID_atend, ID_paciente, CID_10, Cod_manchester, Data_atend FROM Atendimento 
                        ORDER BY ID_atend;""")
                    atendimentos = cursor.fetchall()
            if atendimentos:
                return atendimentos
            else:
                self.erro = f"\nNão há atendimentos"
                return False
        except Error as e:
            self.erro = f"Erro ao listar atendimentos: {e}"
            return False

    def carregar_dados(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""SELECT ID_paciente, cid_10, Cod_manchester, Data_atend FROM Atendimento
                                      WHERE ID_atend = %s;""", (self.id_atend,))
                    dados = cursor.fetchone()
            if dados:
                self.id_paciente, self.cid_10, self.cod_manchester, self.data_atend = dados
                return True
            else:
                self.erro = f"\nAtendimento ID {self.id_atend} não encontrado."
                return False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def atualizar(self, novo_cid_10=None, novo_cod_manchester=None):
        self.cid_10 = novo_cid_10 or self.cid_10
        self.cod_manchester = novo_cod_manchester or self.cod_manchester
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""UPDATE Atendimento SET 
                    CID_10 = %s, COD_manchester = %s WHERE ID_atend = %s;""",
                                   (self.cid_10, self.cod_manchester, self.id_atend))
                    conexao.commit()
            return True
        except Error as e:
            self.erro = f"\nErro ao atualizar atendimento: {str(e)}"
            conexao.rollback()
            return False

    def contar_por_paciente(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM Atendimento WHERE ID_paciente = %s;", (self.id_paciente,))
                    resultado = cursor.fetchone()
            self.erro = f"Não há atendimentos para este paciente."
            return resultado[0] if resultado else False
        except Error as e:
            self.erro = f"\n{e}"
            return False

    def contar_por_cid(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""SELECT COUNT(*) FROM Atendimento 
                    WHERE CID_10 = %s;""", (self.cid_10,))
                    resultado = cursor.fetchone()
            self.erro = ("\nNenhum atendimento encontrado com o CID-10: ", self.cid_10)
            return resultado[0] if resultado else False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def valor_total_tuss(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor as cursor:
                    cursor.execute("""
                    SELECT SUM(Valor) FROM TUSS
                    WHERE Cod_TUSS IN (
                        SELECT ID_tuss FROM Servico
                        WHERE ID_atend = %s
                    );""", self.id_atend)
                    valor = cursor.fetchone()
            self.erro = "\nErro: valor zerado."
            return valor.replace(".", ",") if valor else False
        except Error as e:
            self.erro = f"\nErro ao acessar dados do banco: {str(e)}"
            return False

    def valor_paciente(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor as cursor:
                    cursor.execute("""
                            SELECT SUM(Valor) FROM TUSS
                            WHERE Cod_TUSS IN (
                                SELECT ID_tuss FROM Servico
                                WHERE ID_atend IN (
                                    SELECT ID_atend from Atendimento 
                                    WHERE ID_paciente = %s
                                )
                            );""", (self.id_paciente,))
                    valor = cursor.fetchone()
            self.erro = "\nErro: valor zerado."
            return valor[0].replace(".", ",") if valor else False
        except Error as e:
            self.erro = f"\nErro ao acessar dados do banco: {str(e)}"
            return False
