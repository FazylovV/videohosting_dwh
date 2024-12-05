import os
import pandas as pd
import pyarrow.parquet as prq
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_CONTAINER_PORT")
db_name = os.getenv("DB_NAME")

try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password,
                            host=db_host, port=db_port)

except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Can`t establish connection to database')

df_users = pd.read_sql("SELECT * FROM public.users;", conn)
df_channels = pd.read_sql("SELECT * FROM public.channels;", conn)
df_videos = pd.read_sql("SELECT * FROM public.videos;", conn)
df_likes = pd.read_sql("SELECT * FROM public.likes;", conn)
df_views = pd.read_sql("SELECT * FROM public.views;", conn)

df_users.to_parquet('users.parquet')
df_channels.to_parquet('channels.parquet')
df_videos.to_parquet('videos.parquet')
df_likes.to_parquet('likes.parquet')
df_views.to_parquet('views.parquet')

