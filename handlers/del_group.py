from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.repo import TopicsRepo, Id_UsersRepo

router = Router()

@router.message(Command("delete_group"))
async def send_message_to_group(message: Message):
    for i in Id_UsersRepo.get_users():
        if str(i.id_group) == str(message.message_thread_id):
            Id_UsersRepo.update_group_user(i.telegram_id, None)

    TopicsRepo.delete_topic(message.message_thread_id)
    await message.reply("Чат удален")