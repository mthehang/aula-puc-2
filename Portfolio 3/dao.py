import psycopg2
from psycopg2._psycopg import OperationalError


class BancoDeDados:
    def __init__(self):
        self.parametros_conexao = {
            "host": "aws-0-sa-east-1.pooler.supabase.com",
            "database": "postgres",
            "user": "postgres.kpimaeplwogdjuqoxifx",
            "password": "pucsp@2024*"
        }

    def obter_conexao(self):
        try:
            return psycopg2.connect(**self.parametros_conexao)
        except OperationalError as e:
            print("Não foi possível conectar ao banco de dados:", e)
            return None

    def criar_tabelas(self):
        with self.obter_conexao() as conexao:
            with conexao.cursor() as cursor:

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS Paciente (
                ID_paciente SERIAL PRIMARY KEY,
                RG VARCHAR(20),
                Nome VARCHAR(100),
                Sexo VARCHAR(1),
                Data_nasc DATE,
                Peso INT,
                Altura FLOAT
                );""")

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS Atendimento (
                ID_atend SERIAL PRIMARY KEY,
                ID_paciente INT REFERENCES Paciente(ID_paciente),
                Data_atend TIMESTAMP,
                CID_10 VARCHAR(10)
                );""")

                cursor.execute("""
                CREATE TABLE IF NOT EXISTS CID10 (
                    CAT VARCHAR(10) PRIMARY KEY,
                    DESCR VARCHAR(255)
                );""")

                conexao.commit()


if __name__ == '__main__':
    bd = BancoDeDados()
    bd.criar_tabelas()
