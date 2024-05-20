from datetime import datetime
from psycopg2 import DatabaseError, IntegrityError
from dao import BancoDeDados

bd = BancoDeDados()


class Atendimento:
    def __init__(self, id_paciente, cid_10):
        self.id_atend = None
        self.id_paciente = id_paciente
        self.data_atend = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cid_10 = cid_10

    def salvar(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""SELECT CAT FROM CID10 WHERE CAT = %s;""", (self.cid_10,))
                    if cursor.fetchone() is None:
                        print("\nCID-10 não encontrado! Por favor, insira um CID-10 válido.")
                        return
                    cursor.execute("""INSERT INTO Atendimento (ID_paciente, Data_atend, CID_10) VALUES (%s, %s, %s);""",
                                   (self.id_paciente, self.data_atend, self.cid_10))
                    self.id_atend = cursor.fetchone()[0]
                    conexao.commit()
            print(f"\nAtendimento ID {self.id_atend} adicionado com sucesso na data e hora: {self.data_atend}")
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao salvar atendimento: {e}")

    @staticmethod
    def listar_data(data):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        """SELECT ID_atend, ID_paciente, Data_atend, CID_10 FROM Atendimento 
                        WHERE DATE(Data_atend) = %s ORDER BY ID_atend;""",
                        (data,))
                    atendimentos = cursor.fetchall()
                    if atendimentos:
                        for atendimento in atendimentos:
                            print(
                                f"ID Atendimento: {atendimento[0]}, ID Paciente: {atendimento[1]}, "
                                f"Data: {atendimento[2]}, CID-10: {atendimento[3]}")
                    else:
                        print("Nenhum atendimento encontrado para esta data.")
        except DatabaseError as e:
            print(f"Erro ao listar atendimentos: {e}")

    @staticmethod
    def listar_todos():
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        """SELECT ID_atend, ID_paciente, Data_atend, CID_10 FROM Atendimento ORDER BY ID_atend;""")
                    atendimentos = cursor.fetchall()
                    for atendimento in atendimentos:
                        print(
                            f"ID Atendimento: {atendimento[0]}, ID Paciente: {atendimento[1]}, Data: {atendimento[2]}, "
                            f"CID-10: {atendimento[3]}")
        except DatabaseError as e:
            print(f"Erro ao listar atendimentos: {e}")

    @staticmethod
    def atualizar(id_atend):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""SELECT CID_10 FROM Atendimento WHERE ID_atend = %s;""", (id_atend,))
                    cid_atual = cursor.fetchone()
                    if not cid_atual:
                        print("Atendimento não encontrado!")
                        return

                    print(f"CID-10 atual: {cid_atual[0]}")
                    novo_cid_10 = input("Novo CID-10 (deixe em branco para não alterar): ").strip().upper()
                    if novo_cid_10:
                        cursor.execute("""SELECT CAT FROM CID10 WHERE CAT = %s;""", (novo_cid_10,))
                        if cursor.fetchone() is None:
                            print("\nCID-10 não encontrado! Por favor, insira um CID-10 válido.")
                            return
                    if not novo_cid_10:
                        novo_cid_10 = cid_atual[0]
                    cursor.execute("""UPDATE Atendimento SET CID_10 = %s WHERE ID_atend = %s;""",
                                   (novo_cid_10, id_atend))
                    conexao.commit()
                    print(f"Atendimento {id_atend} atualizado com sucesso. Novo CID-10: {novo_cid_10}")
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao atualizar atendimento: {e}")

    @staticmethod
    def contar_por_paciente(id_paciente):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM Atendimento WHERE ID_paciente = %s;", (id_paciente,))
                    resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        except DatabaseError as e:
            print(f"Erro ao acessar dados do banco: {e}")
            return 0

    @staticmethod
    def contar_por_cid(cid):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM Atendimento WHERE CID_10 = %s;", (cid,))
                    resultado = cursor.fetchone()
            return resultado[0] if resultado else 0
        except DatabaseError as e:
            print(f"Erro ao acessar dados do banco: {e}")
            return 0
