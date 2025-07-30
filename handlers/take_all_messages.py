import asyncio
from aiogram import Router, F
from aiogram.types import Message
from config import Config
from aiogram import types
from help_def.del_message import delete_message_after_delay
from database.repo import Id_UsersRepo
import os

config = Config()
router = Router()


@router.message(F.content_type == types.ContentType.VIDEO)
async def handle_video(message: types.Message):
    id_user = message.from_user.id
    member = await Config.bot.get_chat_member(chat_id=os.environ.get("ID_MAIN_GROUP"), user_id=id_user)
    if member.status == "left":
        if message.from_user.username is None:
            text_to_group = f'Пользователь {message.from_user.full_name} (id: {id_user}):\n'
        else:
            text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\n'
        await config.bot.send_message(
            chat_id=os.environ.get("ID_MAIN_GROUP"),
            message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
            text=text_to_group
        )

        message_id = message.message_id
        from_chat_id = message.chat.id

        await config.bot.copy_message(
            chat_id=os.environ.get("ID_MAIN_GROUP"),
            message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
            from_chat_id=from_chat_id,
            message_id=message_id
        )

        if Id_UsersRepo.get_user(id_user) is None:
            if message.from_user.username is None:
                Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
            else:
                Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)


@router.message(F.content_type == types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    id_user = message.from_user.id
    member = await Config.bot.get_chat_member(chat_id=os.environ.get("ID_MAIN_GROUP"), user_id=id_user)
    if member.status == "left":
        if message.from_user.username is None:
            text_to_group = f'Пользователь {message.from_user.full_name} (id: {id_user}):\n'
        else:
            text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\n'
        await config.bot.send_message(
            chat_id=os.environ.get("ID_MAIN_GROUP"),
            message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
            text=text_to_group
        )

        message_id = message.message_id
        from_chat_id = message.chat.id

        await config.bot.copy_message(
            chat_id=os.environ.get("ID_MAIN_GROUP"),
            message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
            from_chat_id=from_chat_id,
            message_id=message_id
        )

        if Id_UsersRepo.get_user(id_user) is None:
            if message.from_user.username is None:
                Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
            else:
                Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)

@router.message(F.content_type == types.ContentType.VIDEO_NOTE)
async def handle_video_note(message: types.Message):
    id_user = message.from_user.id
    member = await Config.bot.get_chat_member(chat_id=os.environ.get("ID_MAIN_GROUP"), user_id=id_user)
    if member.status == "left":
        if message.from_user.username is None:
            text_to_group = f'Пользователь {message.from_user.full_name} (id: {id_user}):\n'
        else:
            text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\n'
        await config.bot.send_message(
            chat_id=os.environ.get("ID_MAIN_GROUP"),
            message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
            text=text_to_group
        )

        message_id = message.message_id
        from_chat_id = message.chat.id

        await config.bot.copy_message(
            chat_id=os.environ.get("ID_MAIN_GROUP"),
            message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
            from_chat_id=from_chat_id,
            message_id=message_id
        )

        if Id_UsersRepo.get_user(id_user) is None:
            if message.from_user.username is None:
                Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
            else:
                Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)

@router.message()
async def send_message_to_group(message: Message):
    id_user = message.from_user.id
    member = await Config.bot.get_chat_member(chat_id=os.environ.get("ID_MAIN_GROUP"), user_id=id_user)
    if member.status == "left": # member.status == "creator":  # !!!!!!!!!!!! ПРОВЕРКА НА creator ТОЛЬКО НА ВРЕМЯ РАЗРАБОТКИ!!!!!!!!!!!!!!!!!!!!!!!!!!
        text = message.text
        id_user = message.from_user.id

        if Id_UsersRepo.get_user_name(id_user) is not None:
            text_to_group = f'{Id_UsersRepo.get_user_name(id_user)} (id: {id_user}):\n{text}'
        elif message.from_user.username is None:
            text_to_group = f'Новый пользователь {message.from_user.full_name} (id: {id_user}):\n{text}'
        else:
            text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\n{text}'
        await config.bot.send_message(
            chat_id=os.environ.get("ID_MAIN_GROUP"),
            message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
            text=text_to_group
        )

        answer = await config.bot.send_message(
            chat_id=id_user,
            text="Ожидайте ответа"
        )
        await asyncio.create_task(delete_message_after_delay(message.chat.id, answer.message_id))

        if Id_UsersRepo.get_user(id_user) is None:
            if message.from_user.username is None:
                Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
            else:
                Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)
