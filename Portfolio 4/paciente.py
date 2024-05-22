from psycopg2 import Error
from dao import bd
from datetime import datetime


class Paciente:
    def __init__(self, id_paciente=None, rg=None, nome=None, sexo=None, data_nasc=None, peso=None, altura=None):
        self.id_paciente = id_paciente
        self.rg = rg
        self.nome = nome
        self.sexo = sexo
        self.data_nasc = data_nasc
        self.peso = peso
        self.altura = altura
        self.erro = None

    def salvar(self):
        with bd.obter_conexao() as conexao:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    INSERT INTO Paciente (Nome, RG, Sexo, Data_nasc, Peso, Altura) VALUES (%s, %s, %s, %s, %s, %s) 
                    RETURNING ID_paciente;
                    """, (self.nome, self.rg, self.sexo, self.data_nasc, self.peso, self.altura))
                    self.id_paciente = cursor.fetchone()[0]
                    conexao.commit()
                    return True
            except Error as e:
                self.erro = e
                conexao.rollback()
                return False

    def carregar_dados(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""SELECT Nome, RG, Sexo, Data_nasc, Peso, Altura FROM Paciente
                                    WHERE ID_paciente = %s;""", (self.id_paciente,))
                    dados = cursor.fetchone()
                    if dados:
                        self.nome, self.rg, self.sexo, self.data_nasc, self.peso, self.altura = dados
                    else:
                        return False
            return True
        except Error as e:
            self.erro = e
            return -1

    def atualizar(self, novo_nome=None, novo_rg=None, novo_sexo=None, nova_data_nasc=None, novo_peso=None,
                  nova_altura=None):

        self.nome = novo_nome or self.nome
        self.rg = novo_rg or self.rg
        self.sexo = novo_sexo or self.sexo
        self.data_nasc = nova_data_nasc or self.data_nasc
        self.peso = novo_peso or self.peso
        self.altura = nova_altura or self.altura

        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        UPDATE Paciente SET
                        Nome = %s, RG = %s, Sexo = %s, Data_nasc = %s, Peso = %s, Altura = %s
                        WHERE ID_paciente = %s;
                    """, (self.nome, self.rg, self.sexo, self.data_nasc, self.peso, self.altura, self.id_paciente))
                    conexao.commit()
                    return True
        except Error as e:
            self.erro = e
            return False

    @staticmethod
    def listar_todos():
        with bd.obter_conexao() as conexao:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT ID_paciente, Nome, RG, Sexo, Data_nasc, Peso, Altura 
                        FROM Paciente 
                        ORDER BY ID_paciente;
                    """)
                    resultado = cursor.fetchall()
                    if resultado:
                        return resultado
                    else:
                        return False
            except Error:
                return False

    @staticmethod
    def contar_sexo():
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("SELECT Sexo, COUNT(*) FROM Paciente GROUP BY Sexo;")
                    resultados = cursor.fetchall()
            return resultados
        except Error as e:
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
        except Error as e:
            print(f"Erro ao acessar dados do banco: {e}")
            return None

    @staticmethod
    def validar_data(data):
        try:
            datetime.strptime(data, "%Y-%m-%d")
            return True
        except ValueError:
            return False
