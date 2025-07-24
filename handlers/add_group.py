from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.repo import TopicsRepo

router = Router()

@router.message(Command("add_group"))
async def send_message_to_group(message: Message):
    TopicsRepo.add_topic(message.reply_to_message.forum_topic_created.name, message.message_thread_id)
    await message.reply("Чат добавлен")