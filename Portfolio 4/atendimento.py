from datetime import datetime
from psycopg2 import Error
from dao import bd


class Atendimento:
    def __init__(self, id_atend=None, id_paciente=None, cid_10=None,
                 cod_manchester=None, data_atend=datetime.now().strftime('%d/%m/%Y %H:%M')):
        self.id_atend = id_atend
        self.id_paciente = id_paciente
        self.data_atend = data_atend
        self.cid_10 = cid_10
        self.cod_manchester = cod_manchester
        self.erro = None

    def salvar(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        CAT 
                    FROM 
                        CID10 
                    WHERE 
                        CAT = %s;
                    """, (self.cid_10,))
                    if cursor.fetchone() is None:
                        self.erro = f"\nCID-10 {self.cid_10} inválido."
                        return False

                    cursor.execute("""
                    SELECT 
                        1 
                    FROM 
                        Paciente 
                    WHERE 
                        ID_paciente = %s;
                    """, (self.id_paciente,))
                    if cursor.fetchone() is None:
                        self.erro = f"\nID do paciente {self.id_paciente} não encontrado."
                        return False

                    cursor.execute("""
                    SET 
                        datestyle = 'ISO, DMY';
                    """)

                    cursor.execute("""
                    INSERT INTO Atendimento (
                        ID_paciente, 
                        Data_atend, 
                        CID_10
                    )
                    VALUES 
                        (%s, %s, %s) 
                    RETURNING 
                        ID_atend;
                    """,
                                   (self.id_paciente, self.data_atend, self.cid_10))
                    self.id_atend = cursor.fetchone()[0]
                    conexao.commit()
            return True
        except Error as e:
            self.erro = f"\n{str(e)}"
            conexao.rollback()
            return False

    def listar_data(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        ID_atend, 
                        ID_paciente, 
                        to_char(Data_atend, 'DD/MM/YYYY HH24:MI'), 
                        CID_10, 
                        cod_manchester 
                    FROM 
                        Atendimento 
                    WHERE 
                        DATE(Data_atend) = %s 
                    ORDER BY 
                        ID_atend;
                    """, (self.data_atend,))
                    atendimentos = cursor.fetchall()
            if atendimentos:
                return atendimentos
            else:
                self.erro = f"\nNenhum atendimento encontrado para {self.data_atend}."
                return False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def listar_todos(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        ID_atend, ID_paciente, CID_10, Cod_manchester, to_char(Data_atend, 'DD/MM/YYYY') 
                    FROM 
                        Atendimento 
                    ORDER BY 
                        ID_atend;
                    """)
                    atendimentos = cursor.fetchall()
            if atendimentos and not None:
                return atendimentos
            else:
                self.erro = f"\nNenhum atendimento encontrado."
                return False
        except Error as e:
            self.erro = f"Erro ao listar atendimentos: {e}"
            return False

    def carregar_dados(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        ID_paciente, 
                        cid_10, 
                        Cod_manchester, 
                        to_char(Data_atend, 'DD/MM/YYYY H24:MI') 
                    FROM 
                        Atendimento
                    WHERE 
                        ID_atend = %s;
                    """, (self.id_atend,))
                    dados = cursor.fetchone()
            if dados:
                self.id_paciente, self.cid_10, self.cod_manchester, self.data_atend = dados
                return True
            else:
                self.erro = f"\nAtendimento ID {self.id_atend} não encontrado."
                return False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def atualizar(self, novo_cid_10=None, novo_cod_manchester=None):
        self.cid_10 = novo_cid_10 or self.cid_10
        self.cod_manchester = novo_cod_manchester or self.cod_manchester
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        CAT 
                    FROM 
                        CID10 
                    WHERE 
                        CAT = %s;
                    """, (novo_cid_10,))

                    if cursor.fetchone() is None:
                        self.erro = "\nCID-10 não encontrado! Por favor, insira um CID-10 válido."
                        return False

                    cursor.execute("""
                    UPDATE 
                        Atendimento 
                    SET 
                        CID_10 = %s, 
                        COD_manchester = %s 
                    WHERE 
                        ID_atend = %s;
                    """, (self.cid_10, self.cod_manchester, self.id_atend))
                    conexao.commit()
            return True
        except Error as e:
            self.erro = f"\nErro ao atualizar atendimento: {str(e)}"
            conexao.rollback()
            return False

    def contar_por_paciente(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        COUNT(*) 
                    FROM 
                        Atendimento 
                    WHERE 
                        ID_paciente = %s;
                    """, (self.id_paciente,))
                    resultado = cursor.fetchone()
            self.erro = f"Não há atendimentos para este paciente."
            return resultado[0] if resultado else False
        except Error as e:
            self.erro = f"\n{e}"
            return False

    def contar_por_cid(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SELECT 
                        COUNT(*) 
                    FROM 
                        Atendimento 
                    WHERE 
                        CID_10 = %s;
                    """, (self.cid_10,))
                    resultado = cursor.fetchone()
            self.erro = ("\nNenhum atendimento encontrado com o CID-10: ", self.cid_10)
            return resultado[0] if resultado else False
        except Error as e:
            self.erro = f"\n{str(e)}"
            return False

    def valor_total_tuss(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SET 
                        datestyle = 'ISO, DMY';
                    """)
                    cursor.execute("""
                    SELECT 
                        tuss.Descr, 
                        SUM(tuss.Valor) as Valor_Servico,
                        pac.Nome, 
                        pac.ID_paciente, 
                        to_char(atend.data_atend, 'DD/MM/YYYY H24:MI') 
                    FROM 
                        Atendimento atend
                    JOIN 
                        Servico serv ON atend.ID_atend = serv.ID_atend
                    JOIN 
                        TUSS tuss ON serv.ID_tuss = tuss.Cod_TUSS
                    JOIN
                        Paciente pac ON atend.ID_paciente = pac.ID_paciente
                    WHERE 
                        atend.ID_atend = %s
                    GROUP BY 
                        tuss.Descr, pac.Nome, pac.ID_paciente, atend.data_atend;
                    """, (self.id_atend,))
                    resultados = cursor.fetchall()

            if resultados:
                total = sum(item[1] for item in resultados)
                id_paciente = resultados[0][3]
                nome_paciente = resultados[0][2]
                data_atend = resultados[0][4]
                servicos = "\n".join(f"- {item[0]}: R$ {item[1]:.2f}" for item in resultados)
                relatorio = (f"\nAtendimento:"
                             f"\n- ID: {self.id_atend}"
                             f"\n- Data: {data_atend}"
                             f"\nPaciente"
                             f"\n- ID: {id_paciente}"
                             f"\n- Nome: {nome_paciente}"
                             f"\nServiços:\n{servicos}"
                             f"\nTotal: R$ {total:.2f}".replace(".", ","))
                return relatorio
            else:
                self.erro = "Nenhum serviço encontrado para este atendimento."
                return False
        except Error as e:
            self.erro = f"Erro ao acessar dados do banco: {str(e)}"
            return False

    def valor_paciente(self):
        try:
            with bd.obter_conexao() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute("""
                    SET 
                        datestyle = 'ISO, DMY';
                    """)
                    cursor.execute("""
                            SELECT 
                                SUM(tuss.Valor),
                                pac.Nome
                            FROM 
                                Atendimento atend
                            JOIN 
                                Servico serv ON atend.ID_atend = serv.ID_atend
                            JOIN 
                                TUSS tuss ON serv.ID_tuss = tuss.Cod_TUSS
                            JOIN
                                Paciente pac ON atend.ID_paciente = pac.ID_paciente
                            WHERE 
                                atend.ID_paciente = %s
                            GROUP BY 
                                pac.Nome;
                            """, (self.id_paciente,))
                    valor = cursor.fetchone()
            self.erro = "\nErro ao pesquisar paciente: ", self.id_paciente
            return valor if valor else False
        except Error as e:
            self.erro = f"\nErro ao acessar dados do banco: {str(e)}"
            return False
