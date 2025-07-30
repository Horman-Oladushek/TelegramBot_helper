from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.repo import TopicsRepo
from database.repo import Id_UsersRepo

router = Router()

@router.message(Command("add_group"))
async def send_message_to_group(message: Message):
    id_user = message.from_user.id
    if Id_UsersRepo.get_user(id_user) is None:
        if message.from_user.username is None:
            Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
        else:
            Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)
    try:
        TopicsRepo.add_topic(message.reply_to_message.forum_topic_created.name, message.message_thread_id)
        await message.reply("Чат добавлен")
    except Exception as e:
        await message.reply("Чат уже добавлен")