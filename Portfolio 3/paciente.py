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
                cursor.execute("SELECT ID_paciente, Nome, Sexo, Data_nasc FROM Paciente ORDER BY ID_paciente;")
                pacientes = cursor.fetchall()
                for paciente in pacientes:
                    print(f"ID: {paciente[0]}, Nome: {paciente[1]}, Sexo: {paciente[2]}, Data de Nasc.: {paciente[3]}")

    @staticmethod
    def atualizar(id_paciente, novo_nome=None, novo_sexo=None, nova_data_nasc=None, novo_peso=None, nova_altura=None):
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                update_query = """
                UPDATE Paciente SET
                Nome = COALESCE(%s, Nome),
                Sexo = COALESCE(%s, Sexo),
                Data_nasc = COALESCE(%s, Data_nasc),
                Peso = COALESCE(%s, Peso),
                Altura = COALESCE(%s, Altura)
                WHERE ID_paciente = %s;
                """
                cursor.execute(update_query,
                               (novo_nome, novo_sexo, nova_data_nasc, novo_peso, nova_altura, id_paciente))
                conexao.commit()
                print(f"\nCadastro do paciente {id_paciente} atualizado com sucesso.")

    @staticmethod
    def deletar(id_paciente):
        bd = BancoDeDados()
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("DELETE FROM Paciente WHERE ID_paciente = %s;", (id_paciente,))
                conexao.commit()
                print(f"\nPaciente {id_paciente} deletado com sucesso.")
