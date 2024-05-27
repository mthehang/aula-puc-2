from datetime import datetime

from psycopg2 import Error
from dao import bd


class Paciente:
    def __init__(self, id_paciente=None, nome=None, rg=None, sexo=None, data_nasc=None, peso=None, altura=None):
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
                    SET 
                        datestyle = 'ISO, DMY';
                    """)
                    cursor.execute("""
                    INSERT 
                        INTO Paciente (
                            Nome, 
                            RG, 
                            Sexo, 
                            Data_nasc, 
                            Peso, 
                            Altura
                        ) 
                        VALUES 
                            (%s, %s, %s, %s, %s, %s) 
                    RETURNING 
                        ID_paciente;
                    """, (self.nome, self.rg, self.sexo, self.data_nasc, self.peso, self.altura))
                    self.id_paciente = cursor.fetchone()[0]
                    conexao.commit()
                    return True
            except Error as e:
                self.erro = f"\n{str(e)}"
                conexao.rollback()
                return False

    def carregar_dados(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        Nome, 
                        RG, 
                        Sexo, 
                        to_char(Data_nasc, 'DD/MM/YYYY HH24:MI'), 
                        Peso, 
                        Altura 
                    FROM 
                        Paciente
                    WHERE 
                        ID_paciente = %s;
                    """, (self.id_paciente,))
                    dados = cursor.fetchone()
            if dados:
                self.nome, self.rg, self.sexo, self.data_nasc, self.peso, self.altura = dados
                return True
            else:
                self.erro = f"\nPaciente ID {self.id_paciente} não encontrado."
                return False

        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def atualizar(self, novo_nome, novo_rg, novo_sexo, nova_data_nasc, novo_peso,
                  nova_altura):

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
                    SET 
                        datestyle = 'ISO, DMY';
                    """)
                    cursor.execute("""
                    UPDATE 
                        Paciente 
                    SET
                        Nome = %s, 
                        RG = %s, 
                        Sexo = %s, 
                        Data_nasc = %s, 
                        Peso = %s, 
                        Altura = %s
                    WHERE 
                        ID_paciente = %s;
                    """, (self.nome, self.rg, self.sexo, self.data_nasc, self.peso, self.altura, self.id_paciente))
                    conexao.commit()
            return True
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def listar_todos(self):
        with bd.obter_conexao() as conexao:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        ID_paciente, 
                        Nome, 
                        RG, 
                        Sexo, 
                        to_char(Data_nasc, 'DD/MM/YYYY HH24:MI'),
                        Peso, 
                        Altura 
                    FROM 
                        Paciente 
                    ORDER BY 
                        ID_paciente;
                    """)
                    resultado = cursor.fetchall()
                if resultado and not None:
                    return resultado
                else:
                    self.erro = "Nenhum paciente encontrado."
                    return False
            except Error as e:
                self.erro = f"\n{str(e)}"
                return False

    def contar_sexo(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        Sexo, 
                        COUNT(*) 
                    FROM 
                        Paciente 
                    GROUP BY 
                        Sexo;
                    """)
                    resultados = cursor.fetchall()
            if resultados:
                resultados = "\n".join(f"Sexo: {sexo}, Quantidade: {count}" for sexo, count in resultados)
                return resultados
            else:
                self.erro = f"\nNão há dados disponíveis."
                return False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def media_idade(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        AVG (
                            EXTRACT (
                                YEAR FROM AGE (
                                    Data_nasc
                                )
                            )
                        ) 
                    FROM 
                        Paciente;
                    """)
                    resultado = cursor.fetchone()
            if resultado:
                return round(resultado[0], 1)
            else:
                self.erro = "\nNão há dados disponíveis."
                return False
        except Error as e:
            self.erro = e
            return False

    @staticmethod
    def validar_data(data):
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False
