import uuid
from random import randint, shuffle
from faker import Faker
from database_service import db_service

fake = Faker()
videos_id = db_service.get_all_videos_id()
users_to_generate = 99000


def generate_date(start_year: int, end_year: int) -> str:
    year = str(randint(start_year, end_year))
    month = transform_view(randint(1, 12))
    day = transform_view(randint(1, 28))
    return day + "." + month + "." + year


def transform_view(num: int) -> str:
    return str(num) if num >= 10 else "0" + str(num)


def generate_username(custom_url: str) -> str:
    return custom_url.split("@")[1]


def generate_email(username: str) -> str:
    return username + "@gmail.com"


def generate_and_load_user() -> uuid:
    username = fake.user_name()
    while db_service.get_user_id_by_username(username):
        username = fake.user_name()

    email = fake.email()
    while db_service.get_user_id_by_email(email):
        email = fake.email()

    birth_date = generate_date(1985, 2004)
    date_registration = generate_date(2008, 2015)

    db_service.add_user(email, username, birth_date, date_registration)
    return db_service.get_user_id_by_username(username)


def load_like(user_id: uuid, watched_video: uuid, dt_view):
    if randint(1, 3) == 1:
        dt_like = fake.date_time_between_dates(datetime_start=dt_view)
        db_service.add_like(user_id, watched_video, dt_like)


def load_views_and_likes(user_id: uuid):
    chance = randint(1, 5)
    shuffle(videos_id)
    for video_id in videos_id:
        if randint(0, chance) == 0:
            dt_view = fake.date_time_this_month()
            db_service.add_view(user_id, video_id, dt_view)
            load_like(user_id, video_id, dt_view)


def load_actions():
    for i in range(users_to_generate):
        user_id = generate_and_load_user()
        load_views_and_likes(user_id)


# generate_and_load_user()
# load_actions()
