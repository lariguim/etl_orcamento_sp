import psycopg2
import pandas as pd
from datetime import datetime
from transform import transform_despesas, transform_receitas
from extract import extract_despesas, extract_receitas
import logging

# logging
logging.basicConfig(filename='etl_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def create_connection(db_params):
    """ Cria uma conexão com o banco PostgreSQL """
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        logging.info('Conexão com banco de dados PostgreSQL estabelecida.')
    except psycopg2.Error as e:
        logging.error(f'Erro ao conectar ao banco PostgreSQL: {e}')
    return conn

def create_table(conn):
    """ Cria a tabela no banco PostgreSQL """
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS orcamento (
        ID_Fonte_Recurso TEXT,
        Nome_Fonte_Recurso TEXT,
        Total_Liquidado REAL,
        Total_Arrecadado REAL,
        dt_insert TIMESTAMP,
        PRIMARY KEY (ID_Fonte_Recurso, Nome_Fonte_Recurso)
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
        conn.commit()
        logging.info('Tabela criada com sucesso: orcamento')
    except psycopg2.Error as e:
        logging.error(f'Erro ao criar tabela orcamento: {e}')

def insert_data(conn, df_despesas_transform, df_receitas_transform):
    """ Insere os dados transformados na tabela """
    sql_insert = """
    INSERT INTO orcamento (ID_Fonte_Recurso, Nome_Fonte_Recurso, Total_Liquidado, Total_Arrecadado, dt_insert)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (ID_Fonte_Recurso, Nome_Fonte_Recurso) DO UPDATE 
    SET Total_Liquidado = EXCLUDED.Total_Liquidado,
        Total_Arrecadado = EXCLUDED.Total_Arrecadado,
        dt_insert = EXCLUDED.dt_insert;
    """
    try:
        c = conn.cursor()
        for index, row in df_despesas_transform.iterrows():
            data_tuple = (
                row['ID Fonte Recurso'],
                row['Nome Fonte Recurso'],
                row.get('Total Liquidado', None),
                None,
                datetime.now()
            )
            c.execute(sql_insert, data_tuple)
        
        for index, row in df_receitas_transform.iterrows():
            data_tuple = (
                row['ID Fonte Recurso'],
                row['Nome Fonte Recurso'],
                None,
                row.get('Total Arrecadado', None),
                datetime.now()
            )
            c.execute(sql_insert, data_tuple)
        
        conn.commit()
        logging.info('Dados inseridos com sucesso na tabela orcamento.')
    except psycopg2.Error as e:
        logging.error(f'Erro ao inserir dados na tabela orcamento: {e}')

def load_data(df_despesas_transform, df_receitas_transform, db_params):
    """ Função principal para carregar os dados transformados """
    conn = create_connection(db_params)
    if conn is not None:
        try:
            # Cria a tabela se ela não existir
            create_table(conn)
            
            # Insere os dados transformados na tabela
            if not df_despesas_transform.empty or not df_receitas_transform.empty:
                insert_data(conn, df_despesas_transform, df_receitas_transform)
        
        except Exception as e:
            logging.error(f'Erro no processo de carregamento de dados: {e}')
        
        finally:
            conn.close()
            logging.info('Conexão com banco de dados fechada.')

    else:
        logging.error("Erro! Não foi possível conectar ao banco PostgreSQL.")
