import os
import pandas as pd
from pandas import DataFrame
# import matplotlib.pyplot as plt
import psycopg2
from dotenv import load_dotenv
from time import sleep
from airflow import AirflowException
import happybase

load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_CONTAINER_PORT")
db_name = os.getenv("DB_NAME")
hbase_host = "localhost"
hbase_port = 9090


def load_postgres_data():
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
    except:
        raise AirflowException("Can`t establish connection to database")

    df_users = pd.read_sql("SELECT * FROM public.users;", conn)
    df_channels = pd.read_sql("SELECT * FROM public.channels;", conn)
    df_videos = pd.read_sql("SELECT * FROM public.videos;", conn)
    df_likes = pd.read_sql("SELECT * FROM public.likes;", conn)
    df_views = pd.read_sql("SELECT * FROM public.views;", conn)

    return [df_users, df_channels, df_videos, df_likes, df_views]


def make_aggregate_videos(df_videos, df_likes, df_views):
    likes, views = [], []

    for video_id in df_videos["id"]:
        likes.append(len(df_likes[df_likes["video_id"] == video_id]))
        views.append(len(df_views[df_views["video_id"] == video_id]))

    df_videos["views"] = views
    df_videos["likes"] = likes

    return df_videos


def make_aggregate_users(df_users, df_likes, df_views):
    df_users_likes = pd.merge(
        df_users, df_likes, left_on="id", right_on="user_id", how="right"
    )
    df_users_views = pd.merge(
        df_users, df_views, left_on="id", right_on="user_id", how="right"
    )

    df_likes_count = df_users_likes.groupby(["user_id"])
    df_views_count = df_users_views.groupby(["user_id"])
    df_likes_count["count"] = (
        df_users_likes.groupby(["user_id"]).size().to_frame(name="count")
    )
    df_views_count["count"] = (
        df_users_views.groupby(["user_id"]).size().to_frame(name="count")
    )

    df_users.join(df_views_count[["user_id", "count"]], on="user_id")
    df_users.join(df_likes_count[["user_id", "count"]], on="user_id")

    return df_users


def make_aggregate_channels(df_channels, df_aggregate_videos):
    likes, views = [], []

    for channel_id in df_channels["id"]:
        channel_videos = df_aggregate_videos[
            df_aggregate_videos["channel_id"] == channel_id
        ]
        likes.append(sum(channel_videos["likes"]))
        views.append(sum(channel_videos["views"]))
        # axes.append(channel_videos.boxplot(column=["likes", "views"]))
        # plt.savefig('boxplots/' + channel_id + '.jpg')

    df_channels["views"] = views
    df_channels["likes"] = likes

    return df_channels


def load_to_hbase(df_videos, df_channels, df_users):
    connection = happybase.Connection(host=hbase_host, port=hbase_port)
    dfs = {
        'videos': df_videos,
        'channels': df_channels,
        'users': df_users
    }

    for table_name in dfs:
        table = connection.table(table_name)
        columns = dfs[table_name].columns

        for _, row in dfs[table_name].iterrows():
            row_values = {}
            for column in columns:
                row_values[f"cfv:{column}".encode("utf-8")] = \
                    str(row[column]).encode("utf-8")

            table.put(str(row["id"]).encode("utf-8"), row_values)

# def show_boxplot(df_aggregate_videos, column):
#     boxplot = df_aggregate_videos.boxplot(
#         column=[column], by="title_y", rot=45, fontsize=6
#     )
#     # boxplot = df_aggregate_channels.boxplot(column=['likes', 'views'])
#     plt.xlabel('channel_title')
#     plt.ylabel(column)
#     plt.title('')
#     plt.show()


# def get_boxplot_results(df_aggregate_videos):
#     boxplot = df_aggregate_videos.boxplot(column=['likes', 'views'], by='channel_id', rot=45, fontsize=6)
#     print(boxplot)
#     plt.show()


# df_users, df_channels, df_videos, df_likes, df_views = load_postgres_data()
# df_aggregate_videos = make_aggregate_videos(df_videos, df_likes, df_views)
# # df_aggregate_users = make_aggregate_users(df_users, df_likes, df_views)
# df_aggregate_channels = make_aggregate_channels(df_channels, df_aggregate_videos)
# # get_boxplot_results(df_aggregate_videos)
# load_to_hbase(df_aggregate_videos, df_aggregate_channels, df_users)