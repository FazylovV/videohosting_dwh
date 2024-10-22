import uuid

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP, TEXT, BIGINT, UUID, DATE, JSON


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    birth_date: Mapped[str] = mapped_column(DATE)
    date_registration: Mapped[str] = mapped_column(DATE)

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, username={self.username})"


class Channel(Base):
    __tablename__ = "channels"
    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    yt_id: Mapped[str] = mapped_column(String(24))
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(TEXT, nullable=True)
    published_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())


class Video(Base):
    __tablename__ = "videos"
    id: Mapped[int] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"))
    yt_video_id: Mapped[int] = mapped_column(String(11))
    title: Mapped[str] = mapped_column(String(200), nullable=True)
    published_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    description: Mapped[str] = mapped_column(TEXT, nullable=True)


# class Role(Base):
#     __tablename__ = "roles"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     role_name: Mapped[str] = mapped_column(String(15))
#     def __repr__(self) -> str:
#         return f"Role(id={self.id}, role_name={self.role_name})"
#
# class TokenRequest(Base):
#     __tablename__ = "token_requests"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     amount: Mapped[int] = mapped_column()
#     datetime: Mapped[DateTime] = mapped_column(TIMESTAMP, server_default=func.now())
#
#     def __repr__(self) -> str:
#         return f"TokenRequest(id={self.id}, user_id={self.user_id}, amount={self.amount}, datetime={self.datetime}"
#
#
# class Request(Base):
#     __tablename__ = "requests"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
#     video_url: Mapped[str] = mapped_column(String(200), nullable=False)
#     is_favourite: Mapped[bool] = mapped_column(default=False)
#     datetime: Mapped[DateTime] = mapped_column(TIMESTAMP, server_default=func.now())
#     video_information: Mapped[dict] = mapped_column(JSONB, nullable=True)
#     message_id: Mapped[int] = mapped_column()
#     characteristics: Mapped[dict] = mapped_column(JSONB, nullable=True)
#     summary: Mapped[str] = mapped_column(TEXT, nullable=True)
#
#     def __repr__(self) -> str:
#         return f"Request(id={self.id}, user_id={self.user_id}, " \
#                f"video_url={self.video_url}, is_favourite={self.is_favourite}, " \
#                f"datetime={self.datetime}, video_information={self.video_information}, message_id={self.message_id}, " \
#                f"characteristics={self.characteristics}, summary={self.summary})"

# class Data(Base):
#     __tablename__ = "data"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"), unique=True)
#     characteristics: Mapped[str] = mapped_column(JSONB, nullable=True)
#     summary: Mapped[str] = mapped_column(TEXT, nullable=True)
#
#     def  __repr__(self) -> str:
#         return f"Characteristics(request_id={self.request_id}, is_paid={self.is_paid}, data={self.data})"

# class Summary(Base):
#     __tablename__ = "summary"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"), unique=True)
#     data: Mapped[str] = mapped_column(TEXT, nullable=True)
#     is_paid: Mapped[bool] = mapped_column(default=False)
#
#     def __repr__(self) -> str:
#         return f"Summary(request_id={self.request_id}, is_paid={self.is_paid}, data={self.data})"


# class TonalityModel(Base):
#     __tablename__ = "tonality"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     request_id: Mapped[int] = mapped_column(ForeignKey("requests.id"), unique=True)
#     data: Mapped[str] = mapped_column(JSONB, nullable=True)
#     is_paid: Mapped[bool] = mapped_column(default=False)
#
#     def __repr__(self) -> str:
#         return f"Tonality(request_id={self.request_id}, is_paid={self.is_paid}, data={self.data})"
#
# class VideoModel(Base):
#     __tablename__ = "videos"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     video_name: Mapped[str] = mapped_column(String(200), nullable=False)
#     video_url: Mapped[str] = mapped_column(String(200), nullable=False)
#
#     def __repr__(self) -> str:
#         return f"Video(id={self.id}, video_name={self.video_name}, video_url={self.video_url}"
