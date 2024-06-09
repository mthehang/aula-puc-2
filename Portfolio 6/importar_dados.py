import pandas as pd
from psycopg2 import Error
from dao import bd


def ler_excel_para_df(caminho_arquivo):
    return pd.read_excel(caminho_arquivo, engine='openpyxl')


def inserir_dados_cid10(df, nome_tabela):
    try:
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                for _, linha in df.iterrows():
                    cursor.execute(
                        "INSERT INTO {} (CAT, DESCR) VALUES (%s, %s) ON CONFLICT (CAT) DO NOTHING".format(nome_tabela),
                        (linha['CAT'], linha['DESCR'])
                    )
                conexao.commit()
    except Error as e:
        print("Erro: ", e)


def inserir_dados_tuss(df, nome_tabela):
    try:
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                for _, linha in df.iterrows():
                    cursor.execute(
                        f"INSERT INTO {nome_tabela} (Cod_TUSS, Descr, Valor) VALUES (%s, %s, %s) "
                        "ON CONFLICT (Cod_TUSS) DO NOTHING",
                        (linha['COD_TUSS'], linha['DESCR'], linha['vl_ref'])
                    )
                conexao.commit()
    except Error as e:
        print("Erro: ", e)


def importar_especialidades():
    data = {
        "ID": range(1, 20),
        "Especialidade": [
            "Cardiologia", "Dermatologia", "Endocrinologia", "Gastroenterologia",
            "Geriatria", "Ginecologia", "Hematologia", "Infectologia", "Nefrologia",
            "Neurologia", "Oftalmologia", "Oncologia", "Ortopedia", "Otorrinolaringologia",
            "Pediatria", "Pneumologia", "Psiquiatria", "Reumatologia", "Urologia"
        ]
    }

    try:
        with bd.obter_conexao() as conexao:
            with conexao.cursor() as cursor:
                for id_e, especialidade in zip(data["ID"], data["Especialidade"]):
                    cursor.execute("""
                        INSERT INTO Especialidades (ID, Descr) VALUES (%s, %s)
                        ON CONFLICT (ID) DO NOTHING;
                    """, (id_e, especialidade))

                conexao.commit()
        print("Especialidades importadas com sucesso.")

    except Error as e:
        print(f"Erro ao importar especialidades: {e}")
        conexao.rollback()


if __name__ == '__main__':
    """
    caminho_arquivo = 'CID10.xlsx'
    df_cid10 = ler_excel_para_df(caminho_arquivo)
    inserir_dados_cid10(df_cid10, 'CID10')
    print("\nDados CID10 inseridos com sucesso.")

    caminho_arquivo = 'TUSS.xlsx'
    df_tuss = ler_excel_para_df(caminho_arquivo)
    inserir_dados_tuss(df_tuss, 'TUSS')
    print("\nDados TUSS inseridos com sucesso.")
    """
    importar_especialidades()
    