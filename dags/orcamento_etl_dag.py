from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts import etl


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 19),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'orcamento_etl_dag',
    default_args=default_args,
    description='ETL DAG para o orçamento SP',
    schedule_interval=timedelta(days=1),
)

def etl_task():
    etl.main()

run_etl = PythonOperator(
    task_id='run_etl',
    python_callable=etl_task,
    dag=dag,
)

# Adicione a tarefa ao DAG
run_etl
