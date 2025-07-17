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

class Messages(Base):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )


    id_user = sqlalchemy.Column(
        sqlalchemy.String(32),
        sqlalchemy.ForeignKey('id_users.telegram_id')
    )

    message_id = sqlalchemy.Column(
        sqlalchemy.String(32)
    )

    text = sqlalchemy.Column(
        sqlalchemy.String(1024)
    )