import pandas as pd

def extract_despesas():
    try:
        # Carrega o arquivo CSV
        df = pd.read_csv('../data/gdvDespesasExcel.csv', encoding='latin1')
        
        return df
    
    except Exception as e:
        print(f"Erro ao extrair dados de despesas: {e}")
        return None

def extract_receitas():
    try:
        # Carrega o arquivo CSV
        df = pd.read_csv('../data/gdvReceitasExcel.csv', encoding='latin1')
        
        return df
    
    except Exception as e:
        print(f"Erro ao extrair dados de receitas: {e}")
        return None
