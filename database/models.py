import sqlalchemy

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Id_Users(Base):
    __tablename__ = 'id_users'

    telegram_id = sqlalchemy.Column(
        sqlalchemy.String(32),
        primary_key=True,
        unique=True
    )

    username = sqlalchemy.Column(
        sqlalchemy.String(32)
    )

    name_in_chat = sqlalchemy.Column(
        sqlalchemy.String(32)
    )
