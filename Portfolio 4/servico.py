from datetime import datetime
from dao import bd
from psycopg2 import Error


class Servico:
    def __init__(self, id_atend_serv=None, id_atend=None, id_tuss=None,
                 data_serv=datetime.now().strftime('%Y-%m-%d %H:%M')):
        self.id_atend_serv = id_atend_serv
        self.id_atend = id_atend
        self.id_tuss = id_tuss
        self.data_serv = data_serv
        self.erro = None

    def salvar(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SET 
                        datestyle = 'ISO, DMY';
                    """)
                    cursor.execute("""
                    INSERT 
                        INTO Servico (
                            id_atend, 
                            id_tuss, 
                            data_serv
                        )
                    VALUES 
                        (%s, %s, %s);
                    """, (self.id_atend, self.id_tuss, self.data_serv))
                    conexao.commit()
                    return True
        except Error as e:
            self.erro = "Erro ao salvar serviço:", str(e)
            conexao.rollback()
            return False

    def listar_todos(self):
        pass

    def carregar_dados(self):
        pass

    def atualizar(self):
        pass

    def servicos_id_tuss(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            pac.Nome, 
                            
                            to_char(atend.Data_atend, 'DD/MM/YYYY H24:MI'), 
                            SUM(tuss.Valor) AS Valor_Total
                        FROM 
                            Servico serv
                        JOIN 
                            Atendimento atend ON serv.id_atend = atend.ID_atend
                        JOIN 
                            Paciente pac ON atend.ID_paciente = pac.ID_paciente
                        JOIN 
                            TUSS tuss ON serv.id_tuss = tuss.Cod_TUSS
                        WHERE 
                            truss.Cod_TUSS = %s
                        GROUP BY 
                            pac.Nome, 
                            atend.Data_atend;
                        """, (self.id_tuss,))
                    results = cursor.fetchall()
                    self.erro = "Erro ao pesquisar serviços prestados."
                    return results if results else False
        except Error as e:
            self.erro = "Erro: ", str(e)
            return False
