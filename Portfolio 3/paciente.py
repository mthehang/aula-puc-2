from psycopg2 import DatabaseError, IntegrityError
from dao import BancoDeDados

bd = BancoDeDados()


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
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    INSERT INTO Paciente (RG, Nome, Sexo, Data_nasc, Peso, Altura) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING ID_paciente;
                    """, (self.rg, self.nome, self.sexo, self.data_nasc, self.peso, self.altura))
                    self.id_paciente = cursor.fetchone()[0]
                    conexao.commit()
            print(f"\nPaciente adicionado com sucesso. ID: {self.id_paciente}")
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao salvar paciente: {e}")

    @staticmethod
    def listar_todos():
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT ID_paciente, Nome, RG, Sexo, Data_nasc, Peso, Altura 
                        FROM Paciente 
                        ORDER BY ID_paciente;
                    """)
                    pacientes = cursor.fetchall()
                    for paciente in pacientes:
                        print(
                            f"ID: {paciente[0]}, RG: {paciente[1]}, Nome: {paciente[2]}, Sexo: {paciente[3]}, Data de "
                            f"Nascimento: {paciente[4]}, Peso: {paciente[5]} kg, Altura: {paciente[6]} m")
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao listar pacientes: {e}")

    @staticmethod
    def atualizar(id_paciente):
        try:
            with (bd.obter_conexao() as conexao):
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
    def contar_sexo():
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT Sexo, COUNT(*) FROM Paciente GROUP BY Sexo;")
                    resultados = cursor.fetchall()
            return resultados
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao acessar dados do banco: {e}")
            return []

    @staticmethod
    def media_idade():
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT AVG(EXTRACT(YEAR FROM AGE(Data_nasc))) FROM Paciente;")
                    resultado = cursor.fetchone()
            return round(resultado[0], 1) if resultado else None
        except (DatabaseError, IntegrityError) as e:
            print(f"Erro ao acessar dados do banco: {e}")
            return None
