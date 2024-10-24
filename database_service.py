from sqlalchemy import MetaData, create_engine, select
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from model import *

load_dotenv()


class DatabaseService:

    def __init__(self):
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")
        self.engine = create_engine(
            f"postgresql+psycopg2://"
            f"{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def add_channel(self, user_id, yt_id, title, description, published_at):
        with Session(self.engine) as session:
            channel = Channel(
                user_id=user_id,
                yt_id=yt_id,
                title=title,
                description=description,
                published_at=published_at,
            )

            session.add(channel)
            session.commit()

    def get_channel_id_by_yt_id(self, yt_id: str):
        with Session(self.engine) as session:
            result = session.execute(select(Channel.id).where(Channel.yt_id == yt_id))
            channel = result.scalars().first()
            return channel

    def add_video(self, channel_id, yt_video_id, title, published_at, description):
        with Session(self.engine) as session:
            video = Video(
                channel_id=channel_id,
                yt_video_id=yt_video_id,
                title=title,
                published_at=published_at,
                description=description,
            )

            session.add(video)
            session.commit()

    def add_user(self, email, username, birth_date, date_registration):
        with Session(self.engine) as session:
            user = User(
                email=email,
                username=username,
                birth_date=birth_date,
                date_registration=date_registration,
            )

            session.add(user)
            session.commit()

    def add_like(self, user_id, video_id, dt_like):
        with Session(self.engine) as session:
            like = Like(user_id=user_id, video_id=video_id, dt_like=dt_like)

            session.add(like)
            session.commit()

    def add_view(self, user_id, video_id, dt_view):
        with Session(self.engine) as session:
            view = View(user_id=user_id, video_id=video_id, dt_view=dt_view)

            session.add(view)
            session.commit()

    def get_user_id_by_username(self, username: str):
        with Session(self.engine) as session:
            result = session.execute(select(User.id).where(User.username == username))
            user_id = result.scalars().first()
            return user_id

    def get_user_id_by_email(self, email: str):
        with Session(self.engine) as session:
            result = session.execute(select(User.id).where(User.email == email))
            user_id = result.scalars().first()
            return user_id

    def get_all_videos_id(self):
        with Session(self.engine) as session:
            result = session.execute(select(Video.id))
            videos_id = result.scalars().all()
            return videos_id


db_service = DatabaseService()
db_service.create_db()
