import pandas as pd
from dao import BancoDeDados


def ler_excel_para_df(caminho_arquivo):
    return pd.read_excel(caminho_arquivo, engine='openpyxl')


def inserir_dados(df, nome_tabela):
    bd = BancoDeDados()
    with bd.obter_conexao() as conexao:
        with conexao.cursor() as cursor:
            for _, linha in df.iterrows():
                cursor.execute(
                    "INSERT INTO {} (CAT, DESCR) VALUES (%s, %s) ON CONFLICT (CAT) DO NOTHING".format(nome_tabela),
                    (linha['CAT'], linha['DESCR'])
                )
            conexao.commit()


if __name__ == '__main__':
    caminho_arquivo = 'C:\\Users\\Matheus\\Downloads\\CID10.xlsx'
    df_cid10 = ler_excel_para_df(caminho_arquivo)
    inserir_dados(df_cid10, 'CID10')
    print("\nDados inseridos com sucesso.")
