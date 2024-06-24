import pandas as pd
from extract import extract_despesas, extract_receitas
from get_exchange_rate import get_exchange_rate_on_date
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("etl_process.log"),
                        logging.StreamHandler()
                    ])

# Função para limpar os DataFrames
def clean_data(df):
    return df.dropna(subset=['Fonte de Recursos'])

# TRANSFORMAÇÕES
def transform_despesas(df_despesas, exchange_rate):
    try:
        logging.info("Início da transformação de despesas")
        
        # Limpando os dados
        df_despesas = clean_data(df_despesas)
        
        df_despesas = df_despesas.copy()  # Copiando o DataFrame para evitar alterações no original
        
        df_despesas[['ID Fonte Recurso', 'Nome Fonte Recurso']] = df_despesas['Fonte de Recursos'].str.split(' - ', n=1, expand=True)
        df_despesas['Total Liquidado'] = df_despesas['Liquidado'].str.replace('.', '', regex=False)
        df_despesas['Total Liquidado'] = df_despesas['Total Liquidado'].str.replace(',', '.')
        df_despesas['Total Liquidado'] = pd.to_numeric(df_despesas['Total Liquidado'], errors='coerce')
        
        df_despesas = df_despesas[df_despesas['Total Liquidado'].notnull() & (df_despesas['Total Liquidado'] != 0)]
        
        if exchange_rate is not None:
            exchange_rate = pd.to_numeric(exchange_rate, errors='coerce')
            df_despesas.loc[:, 'Total Liquidado'] *= exchange_rate
        
        df_despesas_transform = df_despesas[['ID Fonte Recurso', 'Nome Fonte Recurso', 'Total Liquidado']].copy()
        
        logging.info("Dados de despesas transformados com sucesso")
        return df_despesas_transform
    
    except Exception as e:
        logging.error(f"Erro ao transformar dados de despesas: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

def transform_receitas(df_receitas, exchange_rate):
    try:
        logging.info("Início da transformação de receitas")
        
        # Limpando os dados
        df_receitas = clean_data(df_receitas)
        
        df_receitas = df_receitas.copy()  # Copiando o DataFrame para evitar alterações no original
        
        df_receitas[['ID Fonte Recurso', 'Nome Fonte Recurso']] = df_receitas['Fonte de Recursos'].str.split(' - ', n=1, expand=True)
        df_receitas['Total Arrecadado'] = df_receitas['Arrecadado'].str.replace('.', '', regex=False)
        df_receitas['Total Arrecadado'] = df_receitas['Total Arrecadado'].str.replace(',', '.', regex=False)
        df_receitas['Total Arrecadado'] = pd.to_numeric(df_receitas['Total Arrecadado'], errors='coerce')
        
        df_receitas = df_receitas[df_receitas['Total Arrecadado'].notnull() & (df_receitas['Total Arrecadado'] != 0)]
        
        if exchange_rate is not None:
            exchange_rate = pd.to_numeric(exchange_rate, errors='coerce')
            df_receitas.loc[:, 'Total Arrecadado'] *= exchange_rate
        
        df_receitas_transform = df_receitas[['ID Fonte Recurso', 'Nome Fonte Recurso', 'Total Arrecadado']].copy()
        
        logging.info("Dados de receitas transformados com sucesso")
        return df_receitas_transform
    
    except Exception as e:
        logging.error(f"Erro ao transformar dados de receitas: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

# Executa as transformações 
if __name__ == "__main__":
    try:
        # Extração dos dados
        df_despesas = extract_despesas() 
        df_receitas = extract_receitas()
        exchange_rate = get_exchange_rate_on_date()
        
        # Transformação das despesas
        if df_despesas is not None:
            df_despesas_transform = transform_despesas(df_despesas, exchange_rate)
            if not df_despesas_transform.empty:
                logging.info("Dados de despesas extraídos e transformados com sucesso!")
                print(df_despesas_transform.head())
            else:
                logging.error("Erro na transformação dos dados de despesas ou DataFrame vazio após transformação.")
        
        # Transformação das receitas
        if df_receitas is not None:
            df_receitas_transform = transform_receitas(df_receitas, exchange_rate)
            if not df_receitas_transform.empty:
                logging.info("Dados de receitas extraídos e transformados com sucesso!")
                print(df_receitas_transform.head())
            else:
                logging.error("Erro na transformação dos dados de receitas ou DataFrame vazio após transformação.")
    
    except Exception as e:
        logging.critical(f"Erro crítico no processo ETL: {e}")
