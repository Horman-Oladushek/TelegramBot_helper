from .enigne import EngineController
from .models import Id_Users


class Id_UsersRepo:
    database_controller = EngineController()

    @classmethod
    def add_user(cls, id_user, username):
        session = cls.database_controller.create_session()
        user = Id_Users(telegram_id=id_user, username=username)
        session.add(user)
        session.commit()
        session.close()

    @classmethod
    def get_users(cls):
        session = cls.database_controller.create_session()
        users = session.query(Id_Users).all()
        session.close()
        return users

    @classmethod
    def get_user(cls, id_user):
        session = cls.database_controller.create_session()
        user = session.query(Id_Users).filter_by(telegram_id=id_user).first()
        session.close()
        return user

    @classmethod
    def get_user_name(cls, id_user):
        session = cls.database_controller.create_session()
        name = session.query(Id_Users.name_in_chat).filter_by(telegram_id=id_user).first()
        session.close()
        return name[0]

    @classmethod
    def update_name_user(cls, id_user, name):
        session = cls.database_controller.create_session()
        user = session.query(Id_Users).filter_by(telegram_id=id_user).first()
        user.name_in_chat = name
        session.commit()
        session.close()
