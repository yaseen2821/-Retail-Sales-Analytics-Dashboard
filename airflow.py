from airflow import DAG
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd

def extract_data():
    df = pd.read_csv('path/to/sales_data.csv')
    df.to_json('path/to/sales_data.json', orient='records')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG('retail_sales_dag', default_args=default_args, schedule_interval='@daily') as dag:
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    load_task = S3ToRedshiftOperator(
        task_id='load_to_redshift',
        schema='public',
        table='sales',
        s3_bucket='your-s3-bucket',
        s3_key='sales_data.json',
        copy_options=['JSON 'auto'],
        redshift_conn_id='your_redshift_conn_id',
        aws_conn_id='your_aws_conn_id'
    )

    extract_task >> load_task
