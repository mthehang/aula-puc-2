import pandas as pd
from dao import bd

class ExportarDados:
    def __init__(self):
        self.bd = bd

    def exportar_para_excel(self, view_name, file_name):
        try:
            with self.bd.obter_conexao() as conexao:
                query = f"SELECT * FROM {view_name}"
                df = pd.read_sql_query(query, conexao)
                df.to_excel(file_name, index=False)
                print(f"{view_name} exportado para {file_name} com sucesso.")
        except Exception as e:
            print(f"Erro ao exportar {view_name} para Excel: {e}")

if __name__ == '__main__':
    exportador = ExportarDados()
    views = [
        ("vw_servicos_fora_especialidade", "servicos_fora_especialidade.xlsx"),
        ("vw_quantidade_servicos_por_tipo", "quantidade_servicos_por_tipo.xlsx"),
        ("vw_pacientes_servico_mais_de_uma_vez", "pacientes_servico_mais_de_uma_vez.xlsx"),
        ("vw_servicos_incompativeis_sexo", "servicos_incompativeis_sexo.xlsx"),
        ("vw_servicos_fora_especialidade_medico", "servicos_fora_especialidade_medico.xlsx")
    ]

    for view, file in views:
        exportador.exportar_para_excel(view, file)
