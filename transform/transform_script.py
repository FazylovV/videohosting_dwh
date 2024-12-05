import pandas as pd

df_videos = pd.read_parquet('../extract/videos.parquet')
df_likes = pd.read_parquet('../extract/likes.parquet')
df_views = pd. read_parquet('../extract/views.parquet')

likes = []
views = []

for video_id in df_videos['id']:
    likes.append(len(df_likes[df_likes['video_id'] == video_id]))
    views.append(len(df_views[df_views['video_id'] == video_id]))

df_videos['views'] = views
df_videos['likes'] = likes

df_videos.to_parquet('videos_with_views_and_likes.parquet')