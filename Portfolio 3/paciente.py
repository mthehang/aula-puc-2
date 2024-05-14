<<<<<<< HEAD
from psycopg2._psycopg import DatabaseError, IntegrityError

from dao import BancoDeDados


class Paciente:
    def __init__(self, rg, nome, sexo, data_nasc, peso, altura):
        self.id_paciente = None
        self.rg = rg
        self.nome = nome
        self.sexo = sexo
        self.data_nasc = data_nasc
        self.peso = peso
        self.altura = altura

    def salvar(self):
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                INSERT INTO Paciente (RG, Nome, Sexo, Data_nasc, Peso, Altura) VALUES (%s, %s, %s, %s, %s, %s) RETURNING ID_paciente;
                """, (self.rg, self.nome, self.sexo, self.data_nasc, self.peso, self.altura))
                self.id_paciente = cursor.fetchone()[0]
                conexao.commit()
        print(f"\nPaciente adicionado com sucesso. ID: {self.id_paciente}")

    @staticmethod
    def listar_todos():
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT ID_paciente, RG, Nome, Sexo, Data_nasc, Peso, Altura 
                    FROM Paciente 
                    ORDER BY ID_paciente;
                """)
                pacientes = cursor.fetchall()
                for paciente in pacientes:
                    print(
                        f"ID: {paciente[0]}, RG: {paciente[1]}, Nome: {paciente[2]}, Sexo: {paciente[3]}, Data de "
                        f"Nascimento: {paciente[4]}, Peso: {paciente[5]} kg, Altura: {paciente[6]} m")

    @staticmethod
    def atualizar(id_paciente):
        bd = BancoDeDados()
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        "SELECT Nome, RG, Sexo, Data_nasc, Peso, Altura FROM Paciente WHERE ID_paciente = %s;",
                        (id_paciente,))
                    dados_atuais = cursor.fetchone()
                    if not dados_atuais:
                        print("Paciente não encontrado!")
                        return

                    print(
                        f"Dados Atuais — Nome: {dados_atuais[0]}, RG: {dados_atuais[1]}, Sexo: {dados_atuais[2]}, Data de Nascimento: {dados_atuais[3]}, Peso: {dados_atuais[4]}, Altura: {dados_atuais[5]}")

                    novo_nome = input("Novo nome (deixe em branco para não alterar): ").strip().title() or dados_atuais[
                        0]
                    novo_rg = input("Novo RG (deixe em branco para não alterar): ").strip() or dados_atuais[1]
                    novo_sexo = input("Novo sexo (M/F, deixe em branco para não alterar): ").strip().upper() or \
                                dados_atuais[2]
                    nova_data_nasc = input(
                        "Nova data de nascimento (AAAA-MM-DD, deixe em branco para não alterar): ").strip() or \
                                     dados_atuais[3]

                    novo_peso_input = input("Novo peso (kg, deixe em branco para não alterar): ").strip().replace(',',
                                                                                                                  '.')
                    novo_peso = float(novo_peso_input) if novo_peso_input else dados_atuais[4]

                    nova_altura_input = input("Nova altura (m, deixe em branco para não alterar): ").strip().replace(
                        ',', '.')
                    nova_altura = float(nova_altura_input) if nova_altura_input else dados_atuais[5]

                    cursor.execute("""
                                UPDATE Paciente SET
                                Nome = %s,
                                RG = %s,
                                Sexo = %s,
                                Data_nasc = %s,
                                Peso = %s,
                                Altura = %s
                                WHERE ID_paciente = %s;
                            """, (novo_nome, novo_rg, novo_sexo, nova_data_nasc, novo_peso, nova_altura, id_paciente))
                    conexao.commit()
                    print(f"Cadastro do paciente {id_paciente} atualizado com sucesso.")
        except ValueError:
            print("Valor inválido. Por favor, insira um número válido para peso ou altura.")
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao atualizar dados: {e}")

    @staticmethod
    def deletar(id_paciente):
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("DELETE FROM Paciente WHERE ID_paciente = %s;", (id_paciente,))
                conexao.commit()
                print(f"\nPaciente {id_paciente} deletado com sucesso.")
=======
from psycopg2 import IntegrityError
from psycopg2._psycopg import DatabaseError

from dao import BancoDeDados


class Paciente:
    def __init__(self, rg, nome, sexo, data_nasc, peso, altura):
        self.id_paciente = None
        self.rg = rg
        self.nome = nome
        self.sexo = sexo
        self.data_nasc = data_nasc
        self.peso = peso
        self.altura = altura

    def salvar(self):
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                INSERT INTO Paciente (RG, Nome, Sexo, Data_nasc, Peso, Altura) VALUES (%s, %s, %s, %s, %s, %s) RETURNING ID_paciente;
                """, (self.rg, self.nome, self.sexo, self.data_nasc, self.peso, self.altura))
                self.id_paciente = cursor.fetchone()[0]
                conexao.commit()
        print(f"\nPaciente adicionado com sucesso. ID: {self.id_paciente}")

    @staticmethod
    def listar_todos():
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT ID_paciente, Nome, RG, Sexo, Data_nasc, Peso, Altura FROM Paciente ORDER BY "
                               "ID_paciente;")
                pacientes = cursor.fetchall()
                for paciente in pacientes:
                    print(f"ID: {paciente[0]}, Nome: {paciente[1]}, RG: {paciente[2]}, Sexo: {paciente[3]}, Data de "
                          f"Nasc.: {paciente[4]}, Peso: {paciente[5]} kg, Altura: {paciente[6]} m")

    @staticmethod
    def atualizar(id_paciente):
        bd = BancoDeDados()
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        "SELECT Nome, RG, Sexo, Data_nasc, Peso, Altura FROM Paciente WHERE ID_paciente = %s;",
                        (id_paciente,))
                    dados_atuais = cursor.fetchone()
                    if not dados_atuais:
                        print("Paciente não encontrado!")
                        return

                    print(
                        f"Dados Atuais — Nome: {dados_atuais[0]}, RG: {dados_atuais[1]}, Sexo: {dados_atuais[2]}, "
                        f"Data de Nascimento: {dados_atuais[3]}, Peso: {dados_atuais[4]}, Altura: {dados_atuais[5]}")

                    novo_nome = input("Novo nome (deixe em branco para não alterar): ").strip().title() or dados_atuais[
                        0]
                    novo_rg = input("Novo RG (deixe em branco para não alterar): ").strip() or dados_atuais[1]
                    novo_sexo = input("Novo sexo (M/F, deixe em branco para não alterar): ").strip().upper() or \
                                dados_atuais[2]
                    nova_data_nasc = input(
                        "Nova data de nascimento (AAAA-MM-DD, deixe em branco para não alterar): ").strip() or \
                                     dados_atuais[3]

                    novo_peso = None
                    while novo_peso is None:
                        peso_input = input("Novo peso (kg, deixe em branco para não alterar): ").strip().replace(',',
                                                                                                                 '.')
                        if not peso_input:
                            novo_peso = dados_atuais[4]
                        else:
                            try:
                                novo_peso = float(peso_input)
                            except ValueError:
                                print("Valor inválido. Por favor, insira um número válido para o peso.")
                                continue

                    nova_altura = None
                    while nova_altura is None:
                        altura_input = input("Nova altura (m, deixe em branco para não alterar): ").strip().replace(',',
                                                                                                                    '.')
                        if not altura_input:
                            nova_altura = dados_atuais[5]
                        else:
                            try:
                                nova_altura = float(altura_input)
                            except ValueError:
                                print("Valor inválido. Por favor, insira um número válido para a altura.")
                                continue

                    cursor.execute("""
                                UPDATE Paciente SET
                                Nome = %s,
                                RG = %s,
                                Sexo = %s,
                                Data_nasc = %s,
                                Peso = %s,
                                Altura = %s
                                WHERE ID_paciente = %s;
                            """, (novo_nome, novo_rg, novo_sexo, nova_data_nasc, novo_peso, nova_altura, id_paciente))
                    conexao.commit()
                    print(f"Cadastro do paciente {id_paciente} atualizado com sucesso.")
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao atualizar dados: {e}")

    @staticmethod
    def deletar(id_paciente):
        bd = BancoDeDados()
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("DELETE FROM Paciente WHERE ID_paciente = %s;", (id_paciente,))
                    if cursor.rowcount == 0:
                        print("Nenhum paciente encontrado para deletar.")
                    else:
                        conexao.commit()
                        print(f"\nPaciente {id_paciente} deletado com sucesso.")
        except DatabaseError as e:
            print(f"Erro ao deletar paciente: {e}")
>>>>>>> 66df591460bbc2b0ed74e6b39f473d193ee07fdd
