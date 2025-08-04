from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.repo import TopicsRepo
from help_def.add_new_user_to_db import add_new_user_to_bd

router = Router()

@router.message(Command("add_group"))
async def send_message_to_group(message: Message):
    add_new_user_to_bd(message.from_user.id, message)
    if message.chat.type != "private":
        TopicsRepo.add_topic(message.reply_to_message.forum_topic_created.name, message.message_thread_id)
        await message.reply('Чат добавлен')
        try:
            TopicsRepo.add_topic(message.reply_to_message.forum_topic_created.name, message.message_thread_id)
            await message.reply("Чат добавлен")
        except Exception as e:
            await message.reply("Чат уже добавлен")