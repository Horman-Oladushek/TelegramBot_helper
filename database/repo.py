from .enigne import EngineController
from .models import Id_Users, Topics


class Id_UsersRepo:
    database_controller = EngineController()

    @classmethod
    def add_user(cls, id_user, username, name_in_chat=None, id_group=None):
        session = cls.database_controller.create_session()
        user = Id_Users(telegram_id=id_user, username=username, name_in_chat=name_in_chat, id_group=id_group)
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

    @classmethod
    def update_group_user(cls, id_user, group):
        session = cls.database_controller.create_session()
        user = session.query(Id_Users).filter_by(telegram_id=id_user).first()
        user.id_group = group
        session.commit()
        session.close()

class TopicsRepo:
    database_controller = EngineController()

    @classmethod
    def add_topic(cls, name_topic, id_topic):
        session = cls.database_controller.create_session()
        topic = Topics(name_topic=name_topic, id_topic=id_topic)
        session.add(topic)
        session.commit()
        session.close()

    @classmethod
    def get_topics(cls):
        session = cls.database_controller.create_session()
        topics = session.query(Topics).all()
        session.close()
        return topics

    @classmethod
    def get_topic(cls, id_topic=None):
        session = cls.database_controller.create_session()
        topic = session.query(Topics).filter_by(id_topic=id_topic).first()
        session.close()
        return topic

    @classmethod
    def delete_topic(cls, id_topic):
        session = cls.database_controller.create_session()
        session.query(Topics).filter_by(id_topic=id_topic).delete()
        session.commit()
        session.close()