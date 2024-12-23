from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.decorators import task
import pandas as pd
from pandas import DataFrame
from etl_utils import (
    load_postgres_data,
    make_aggregate_videos,
    make_aggregate_channels,
    make_aggregate_users,
    load_to_hbase
)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

@task.python
def extract_from_postgres():
    return load_postgres_data()

@task.python
def make_videos_aggregate(dataframes):
    df_videos, df_likes, df_views = dataframes[2], dataframes[3], dataframes[4]
    return make_aggregate_videos(df_videos, df_likes, df_views)

@task.python
def make_channels_aggregate(dataframes, df_aggregate_videos):
    df_channels = dataframes[1]
    return make_aggregate_channels(df_channels, df_aggregate_videos)

@task.python
def make_users_aggregate(dataframes):
    df_users, df_likes, df_views = dataframes[0], dataframes[3], dataframes[4]
    return make_aggregate_users(df_users, df_likes, df_views)

@task.python
def load_hbase(df_aggregate_videos, df_aggreagate_channels, df_aggregate_users):
    load_to_hbase(df_aggregate_videos, df_aggreagate_channels, df_aggregate_users)

with DAG(
    "videohosting_etl_pipeline",
    default_args=default_args,
    description="DAG for processing videohosting data",
    schedule_interval="@daily",
) as dag:
    dataframes = extract_from_postgres()
    df_aggregate_videos = make_videos_aggregate(dataframes)
    df_aggregate_channels = make_channels_aggregate(dataframes, df_aggregate_videos)
    df_aggregate_users = make_users_aggregate(dataframes)
    load_hbase(df_aggregate_videos, df_aggregate_channels, df_aggregate_users)
