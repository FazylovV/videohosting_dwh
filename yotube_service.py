import requests
from pytube import YouTube

import generator
from json_parser import *

load_dotenv()
YT_api_key = os.getenv("YT_API_KEY")


class YoutubeService:
    # async def get_video_comments(self, video_url) -> (list, int):
    #     video_id = self.get_video_code(video_url)
    #     comments = []
    #     youtube = build('youtube', 'v3', developerKey=YT_api_key)
    #     video_response = youtube.commentThreads().list(
    #         part='snippet,replies',
    #         videoId=video_id
    #     ).execute()
    #     comment_count = 0
    #     while video_response:
    #         for item in video_response['items']:
    #             comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
    #             repl = ""
    #             comment_count += 1
    #             replycount = item['snippet']['totalReplyCount']
    #             if replycount > 0:
    #                 repl = " ответы на комментарий: [ "
    #                 for reply in item['replies']['comments']:
    #                     repl += reply['snippet']['textDisplay']
    #                 repl += " ]"
    #             comments.append(comment + repl)
    #             print(comment)
    #
    #         if 'nextPageToken' in video_response and comment_count < 50000:
    #             video_response = youtube.commentThreads().list(
    #                 part='snippet,replies',
    #                 videoId=video_id,
    #                 pageToken=video_response['nextPageToken']
    #             ).execute()
    #         else:
    #             break
    #     return comments, comment_count

    def get_channel(self, channel_id: str):
        url = (
            f"https://youtube.googleapis.com/youtube/v3/channels?"
            f"part=snippet&part=statistics&id={channel_id}&key={YT_api_key}"
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.json())

    def load_user(self, custom_url: str):
        username = generator.generate_username(custom_url)
        user_id = db_service.get_user_id_by_username(username)
        if not user_id:
            email = generator.generate_email(username)
            birth_date = generator.generate_date(1985, 2004)
            date_registration = generator.generate_date(2008, 2015)
            db_service.add_user(email, username, birth_date, date_registration)
            user_id = db_service.get_user_id_by_username(username)
        return user_id

    def load_channel(self, yt_channel_id: str, user_id: str, channel_data: dict):
        channel_id = db_service.get_channel_id_by_yt_id(yt_channel_id)
        if not channel_id:
            title, description, published_at = parse_channel(channel_data)
            db_service.add_channel(
                user_id, yt_channel_id, title, description, published_at
            )
            channel_id = db_service.get_channel_id_by_yt_id(yt_channel_id)
            print(title)
        return channel_id

    def load_video(self, video_data: dict, channel_id: str):
        yt_video_id, title, description, published_at = parse_video(video_data)
        db_service.add_video(channel_id, yt_video_id, title, published_at, description)
        print(title + "\n")

    def load_videos(self):
        video_category_id = 10
        chart = "mostPopular"
        url = (
            f"https://youtube.googleapis.com/youtube/v3/"
            f"videos?part=statistics&part=snippet&chart={chart}"
            f"&videoCategoryId={video_category_id}&key={YT_api_key}"
        )
        response = requests.get(url)
        video_count = 0
        while response:
            data = response.json()
            for item in data["items"]:
                snippet = item["snippet"]
                yt_channel_id = snippet["channelId"]
                channel_data = self.get_channel(yt_channel_id)

                try:
                    custom_url = channel_data["items"][0]["snippet"]["customUrl"]
                except:
                    continue

                user_id = self.load_user(
                    channel_data["items"][0]["snippet"]["customUrl"]
                )
                channel_id = self.load_channel(yt_channel_id, user_id, channel_data)
                self.load_video(item, channel_id)

                video_count += 1

            if "nextPageToken" in data and video_count < 20:
                url = (
                    f"https://youtube.googleapis.com/youtube/v3/"
                    f"videos?part=statistics&part=snippet&chart={chart}"
                    f"&videoCategoryId={video_category_id}"
                    f'&pageToken={data["nextPageToken"]}&key={YT_api_key}'
                )
                response = requests.get(url)
            else:
                break
        print(response.json())

    def download(self):
        YouTube("https://youtube.com/watch?v=UjpqFDhCKIc").streams.filter(
            progressive=True, file_extension="mp4"
        ).first().download()


yt_service = YoutubeService()
yt_service.load_videos()

# yt.load_videos_by_channel_id('UCq-Fj5jknLsUf-MWSy4_brA')
