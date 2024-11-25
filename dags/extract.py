from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from pyspark.sql import SparkSession
import os

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .master(f"spark://172.18.0.6:7077") \
    .getOrCreate()

dag = DAG(
    "extract_postgres_and_minio_to_iceberg",
    default_args=default_args,
    description="extracts data from PostgreSQL and MinioS3 and saves it to Apache Iceberg",
    schedule_interval=None,
)

def create_spark_session():
    # print(spark.active)
    print('Hello')

create_session_task = PythonOperator(
    task_id="create_spark_session",
    python_callable=create_spark_session,
    dag=dag
)

(
    create_session_task
)
