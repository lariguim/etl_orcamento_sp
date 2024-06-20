import scripts.extract
import scripts.load_data
import scripts.transform
import scripts.get_exchange_rate
import logging
from scripts import extract

# logging 
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("etl_process.log"),
                        logging.StreamHandler()
                    ])

# Parâmetros de conexão ao banco de dados PostgreSQL
db_params = {
    'dbname': 'orcamento_sp',
    'user': 'larissa',
    'host': 'localhost',
    'port': 5432
}

def main():
    try:
        despesas_df = extract.extract_despesas()
        receitas_df = extract.extract_receitas()
        
        if despesas_df is None or receitas_df is None:
            logging.error("Erro ao extrair dados. Verifique os arquivos e tente novamente.")
            return
        
        exchange_rate = get_exchange_rate.get_exchange_rate_on_date()
        
        if exchange_rate is None:
            logging.error("Erro ao obter a taxa de câmbio. Verifique a conexão com a API.")
            return
        
        df_despesas_transform = transform.transform_despesas(despesas_df, exchange_rate)
        df_receitas_transform = transform.transform_receitas(receitas_df, exchange_rate)
        
        if df_despesas_transform.empty and df_receitas_transform.empty:
            logging.error("Erro ao transformar os dados.")
            return
        
        load_data.load_data(df_despesas_transform, df_receitas_transform, db_params)
        
        logging.info("Processo ETL concluído com sucesso!")
    
    except Exception as e:
        logging.error(f'Erro durante o processo ETL: {e}')

if __name__ == "__main__":
    main()
