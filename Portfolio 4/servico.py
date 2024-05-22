from datetime import datetime
from dao import bd
from psycopg2 import Error


class Servico:
    def __init__(self, id_atend, id_tuss):
        self.id_atend_serv = None
        self.id_atend = id_atend
        self.id_tuss = id_tuss
        self.data_serv = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def salvar(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Servico (id_atend, id_tuss, data_serv)
                        VALUES (%s, %s, %s);
                    """, (self.id_atend, self.id_tuss, self.data_serv))
                    conexao.commit()
                    print("Serviço cadastrado com sucesso.")
        except Error as e:
            print("Erro ao salvar serviço:", e)
            conexao.rollback()

    @staticmethod
    def servicos_prestados(cod_tuss):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            Paciente.Nome, 
                            Atendimento.Data_atend, 
                            SUM(TUSS.Valor) AS Valor_Total
                        FROM 
                            Servico
                        JOIN 
                            Atendimento ON Servico.id_atend = Atendimento.ID_atend
                        JOIN 
                            Paciente ON Atendimento.ID_paciente = Paciente.ID_paciente
                        JOIN 
                            TUSS ON Servico.id_tuss = TUSS.Cod_TUSS
                        WHERE 
                            TUSS.Cod_TUSS = %s
                        GROUP BY 
                            Paciente.Nome, 
                            Atendimento.Data_atend
                        ;""", (cod_tuss,))
                    results = cursor.fetchall()
                    for result in results:
                        print(f"Nome: {result[0]}, Data do Atendimento: {result[1]}, Valor Total: {result[2]}")
        except Error as e:
            print("Erro: ", e)
