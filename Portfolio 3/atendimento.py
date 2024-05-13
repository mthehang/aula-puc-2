from dao import BancoDeDados
from datetime import datetime


class Atendimento:
    def __init__(self, id_paciente, cid_10):
        self.id_paciente = id_paciente
        self.data_atend = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cid_10 = cid_10

    def salvar(self):
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT CAT FROM CID10 WHERE CAT = %s;", (self.cid_10,))
                if cursor.fetchone() is None:
                    print("\nCID-10 não encontrado! Por favor, insira um CID-10 válido.")
                    return
                cursor.execute("INSERT INTO Atendimento (ID_paciente, Data_atend, CID_10) VALUES (%s, %s, %s);",
                               (self.id_paciente, self.data_atend, self.cid_10))
                conexao.commit()
        print("\nAtendimento adicionado com sucesso na data e hora:", self.data_atend)

    @staticmethod
    def listar_todos():
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT ID_atend, ID_paciente, Data_atend, CID_10 FROM Atendimento ORDER BY ID_atend;")
                atendimentos = cursor.fetchall()
                for atendimento in atendimentos:
                    print(
                        f"ID Atendimento: {atendimento[0]}, ID Paciente: {atendimento[1]}, Data: {atendimento[2]}, CID-10: {atendimento[3]}")

    @staticmethod
    def deletar(id_atend):
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("DELETE FROM Atendimento WHERE ID_atend = %s;", (id_atend,))
                conexao.commit()
                print(f"\nAtendimento {id_atend} deletado com sucesso.")
