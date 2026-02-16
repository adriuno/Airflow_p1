import os
import datetime
import pendulum
import requests

from airflow.sdk import dag, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


@dag(
    dag_id="process_employees",
    schedule=None,  # luego "0 0 * * *"
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def process_employees():

    @task
    def get_data():
        data_path = "/opt/airflow/dags/files/employees.csv"
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

        url = "https://raw.githubusercontent.com/apache/airflow/main/airflow-core/docs/tutorial/pipeline_example.csv"
        r = requests.get(url, timeout=30)
        r.raise_for_status()

        with open(data_path, "w", encoding="utf-8") as f:
            f.write(r.text)

        hook = PostgresHook(postgres_conn_id="tutorial_pg_conn")
        conn = hook.get_conn()
        cur = conn.cursor()

        cur.execute("TRUNCATE TABLE employees_temp;")

        with open(data_path, "r", encoding="utf-8") as f:
            cur.copy_expert(
                "COPY employees_temp FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
                f,
            )
        conn.commit()

    merge = SQLExecuteQueryOperator(
        task_id="merge_employees",
        conn_id="tutorial_pg_conn",
        sql="merge_employees.sql",
    )

    get_data() >> merge


dag = process_employees()
