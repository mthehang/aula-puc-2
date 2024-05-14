<<<<<<< HEAD
from dao import BancoDeDados

bd = BancoDeDados()


def contar_pacientes_por_sexo():
    with bd.obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT Sexo, COUNT(*) FROM Paciente GROUP BY Sexo;")
            resultados = cursor.fetchall()
    return resultados


def contar_atendimentos_por_paciente(id_paciente):
    with bd.obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Atendimento WHERE ID_paciente = %s;", (id_paciente,))
            resultado = cursor.fetchone()
    return resultado[0] if resultado else 0


def contar_atendimentos_por_cid(cid):
    with bd.obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Atendimento WHERE CID_10 = %s;", (cid,))
            resultado = cursor.fetchone()
    return resultado[0] if resultado else 0


def calcular_media_idade_pacientes():
    with bd.obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT AVG(EXTRACT(YEAR FROM AGE(Data_nasc))) FROM Paciente;")
            resultado = cursor.fetchone()
    return round(resultado[0], 1) if resultado else None
=======
from dao import BancoDeDados
from psycopg2 import DatabaseError

bd = BancoDeDados()


def contar_pacientes_por_sexo():
    try:
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT Sexo, COUNT(*) FROM Paciente GROUP BY Sexo;")
                resultados = cursor.fetchall()
        return resultados
    except DatabaseError as e:
        print(f"Erro ao acessar dados do banco: {e}")
        return []


def contar_atendimentos_por_paciente(id_paciente):
    try:
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Atendimento WHERE ID_paciente = %s;", (id_paciente,))
                resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    except DatabaseError as e:
        print(f"Erro ao acessar dados do banco: {e}")
        return 0


def contar_atendimentos_por_cid(cid):
    try:
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM Atendimento WHERE CID_10 = %s;", (cid,))
                resultado = cursor.fetchone()
        return resultado[0] if resultado else 0
    except DatabaseError as e:
        print(f"Erro ao acessar dados do banco: {e}")
        return 0


def calcular_media_idade_pacientes():
    try:
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT AVG(EXTRACT(YEAR FROM AGE(Data_nasc))) FROM Paciente;")
                resultado = cursor.fetchone()
        return round(resultado[0], 1) if resultado else None
    except DatabaseError as e:
        print(f"Erro ao acessar dados do banco: {e}")
        return None
>>>>>>> 66df591460bbc2b0ed74e6b39f473d193ee07fdd
