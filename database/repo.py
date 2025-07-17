from .enigne import EngineController
from .models import Id_Users, Messages

class MessagesRepo:
    database_controller = EngineController()

    @classmethod
    def add_message(cls, id_user, message_id, text):
        session = cls.database_controller.create_session()
        message = Messages(id_user=id_user, message_id=message_id, text=text)
        session.add(message)
        session.commit()
        session.close()

    @classmethod
    def get_messages(cls):
        session = cls.database_controller.create_session()
        messages = session.query(Messages).all()
        session.close()
        return messages

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