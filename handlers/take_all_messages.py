from aiogram import Router, F
from aiogram.types import Message
from config import Config
from database.repo import MessagesRepo, Id_UsersRepo
from aiogram import types
import os
import uuid

config = Config()
router = Router()


@router.message(F.content_type == types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    local_id_message = str(uuid.uuid4())

    id_user = message.from_user.id

    if message.from_user.username is None:
        text_to_group = f'Пользователь {message.from_user.full_name} (id: {id_user}):\n'
    else:
        text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\n'
    await config.bot.send_message(
        chat_id=os.environ.get("ID_GROUP"),
        text=text_to_group
    )

    message_id = message.message_id
    photo = message.photo[-1]

    file_id = photo.file_id
    file = await config.bot.get_file(file_id)
    file_path = file.file_path
    if not os.path.exists('photos'):
        os.makedirs('photos')
    await config.bot.download_file(file_path, f'photos/{local_id_message}.jpg')

    from_chat_id = message.chat.id

    await config.bot.copy_message(
        chat_id=os.environ.get("ID_GROUP"),
        from_chat_id=from_chat_id,
        message_id=message_id
    )
    MessagesRepo.add_message(id_user=id_user, message_id=local_id_message, text=message.caption)
    if Id_UsersRepo.get_user(id_user) is None:
        Id_UsersRepo.add_user(id_user, (f'@{message.from_user.username}' or message.from_user.full_name))



@router.message()
async def send_message_to_group(message: Message):
    text = message.text
    id_user = message.from_user.id

    if message.from_user.username is None:
        text_to_group = f'Пользователь {message.from_user.full_name} (id: {id_user}):\n{text}'
    else:
        text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\n{text}'
    await config.bot.send_message(
        chat_id=os.environ.get("ID_GROUP"),
        text=text_to_group
    )

    await config.bot.send_message(
        chat_id=id_user,
        text="Ожидайте ответа"
    )

    MessagesRepo.add_message(id_user=id_user, message_id=str(uuid.uuid4()), text=text)
    if Id_UsersRepo.get_user(id_user) is None:
        Id_UsersRepo.add_user(id_user, (f'@{message.from_user.username}' or message.from_user.full_name))



