from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

with DAG(
    dag_id="create_tables_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,   # manual
    catchup=False,
) as dag:

    create_tables = SQLExecuteQueryOperator(
        task_id="create_tables",
        conn_id="tutorial_pg_conn",     # IMPORTANTE: que exista esa conexión en Airflow
        sql="create_tables.sql",        # el archivo .sql que está dentro de dags/
    )
