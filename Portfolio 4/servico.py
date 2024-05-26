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
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        ID_atend_serv,
                        ID_atend, 
                        ID_tuss, 
                        to_char(Data_serv, 'DD/MM/YYYY HH24:MI')
                    FROM 
                        Servico
                    ORDER BY 
                        ID_atend_serv;
                    """)
                    servicos = cursor.fetchall()
            if servicos and not None:
                return servicos
            else:
                self.erro = f"\nNenhum serviço encontrado."
                return False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    # arrumar defs servico
    def carregar_dados(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        Nome, 
                        RG, 
                        Sexo, 
                        to_char(Data_nasc, 'DD/MM/YYYY'), 
                        Peso, 
                        Altura 
                    FROM 
                        Paciente
                    WHERE 
                        ID_paciente = %s;
                    """, (self.id_atend_serv,))
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

    def atualizar(self, id_atend_serv, id_atend, id_tuss):
        self.id_atend_serv = id_atend_serv or self.id_atend_serv
        self.id_atend = id_atend or self.id_atend
        self.id_tuss = id_tuss or self.id_tuss

        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SET 
                        datestyle = 'ISO, DMY';
                    """)
                    cursor.execute("""
                    UPDATE 
                        Servico 
                    SET
                        ID_atend = %s, 
                        ID_tuss = %s
                    WHERE 
                        ID_atend_serv = %s;
                    """, self.id_atend_serv)
                    conexao.commit()
            return True
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

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

    def servico_data(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                        SELECT 
                            tuss.Cod_TUSS, 
                            pac.Sexo, 
                            COUNT(serv.ID_atend) AS Quantidade,
                            SUM(tuss.Valor) AS Valor_Total
                        FROM 
                            Servico serv
                        JOIN 
                            Atendimento atend ON serv.ID_atend = atend.ID_atend
                        JOIN 
                            Paciente pac ON atend.ID_paciente = pac.ID_paciente
                        JOIN 
                            TUSS tuss ON serv.ID_tuss = tuss.Cod_TUSS
                        WHERE 
                            tuss.Cod_TUSS = %s
                        GROUP BY 
                            tuss.Cod_TUSS, pac.Sexo;
                    """, (self.id_tuss,))
                    results = cursor.fetchall()
                    return results if results else False
        except Error as e:
            self.erro = f"Erro: {str(e)}"
            return False

