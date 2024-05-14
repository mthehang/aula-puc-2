from dao import BancoDeDados
from datetime import datetime
from psycopg2 import DatabaseError, IntegrityError


class Atendimento:
    def __init__(self, id_paciente, cid_10):
        self.id_paciente = id_paciente
        self.data_atend = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cid_10 = cid_10

    def salvar(self):
        bd = BancoDeDados()
        try:
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
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao salvar atendimento: {e}")

    @staticmethod
    def atualizar(id_atend):
        bd = BancoDeDados()
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT CID_10 FROM Atendimento WHERE ID_atend = %s;", (id_atend,))
                    cid_atual = cursor.fetchone()
                    if not cid_atual:
                        print("Atendimento não encontrado!")
                        return

                    print(f"CID-10 atual: {cid_atual[0]}")
                    novo_cid_10 = input("Novo CID-10 (deixe em branco para não alterar): ").strip().upper()
                    if novo_cid_10:
                        cursor.execute("SELECT CAT FROM CID10 WHERE CAT = %s;", (novo_cid_10,))
                        if cursor.fetchone() is None:
                            print("\nCID-10 não encontrado! Por favor, insira um CID-10 válido.")
                            return
                    if not novo_cid_10:
                        novo_cid_10 = cid_atual[0]
                    cursor.execute("UPDATE Atendimento SET CID_10 = %s WHERE ID_atend = %s;", (novo_cid_10, id_atend))
                    conexao.commit()
                    print(f"Atendimento {id_atend} atualizado com sucesso. Novo CID-10: {novo_cid_10}")
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao atualizar atendimento: {e}")

    @staticmethod
    def deletar(id_atend):
        bd = BancoDeDados()
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("DELETE FROM Atendimento WHERE ID_atend = %s;", (id_atend,))
                    if cursor.rowcount == 0:
                        print("Nenhum atendimento encontrado para deletar.")
                    else:
                        conexao.commit()
                        print(f"\nAtendimento {id_atend} deletado com sucesso.")
        except DatabaseError as e:
            print(f"Erro ao deletar atendimento: {e}")
