"""Illustrative Airflow DAG (not executed in this demo): refresh then build, daily, with retries."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

import pipeline

with DAG(
    "daily_report",
    start_date=datetime(2025, 1, 1),
    schedule="0 9 * * *",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
) as dag:
    refresh = PythonOperator(task_id="refresh", python_callable=pipeline.refresh)
    build = PythonOperator(task_id="build_deck", python_callable=pipeline.build_deck)
    refresh >> build
