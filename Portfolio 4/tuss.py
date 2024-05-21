from dao import BancoDeDados
from datetime import datetime


class Servico:
    bd = BancoDeDados()

    def __init__(self, id_atend):
        self.id_atend_serv = None
        self.id_atend = id_atend
        self.id_tuss = id_tuss
        self.data_serv = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

