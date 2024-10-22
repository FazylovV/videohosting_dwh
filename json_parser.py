import json

# from yotube_service import *
from database_service import *


def parse_channel(data: dict) -> (str, str, str):
    item = data["items"][0]
    snippet = item["snippet"]
    title = snippet["title"]
    description = snippet["description"]
    published_at = snippet["publishedAt"]
    return title, description, published_at


def parse_video(data: dict):
    video_id = data["id"]
    snippet = data["snippet"]
    title = snippet["title"]
    description = snippet["description"]
    published_at = snippet["publishedAt"]
    return video_id, title, description, published_at


# def parse_videos()
# parse_data_to_db()
