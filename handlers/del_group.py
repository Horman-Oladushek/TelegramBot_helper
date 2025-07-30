from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.repo import TopicsRepo, Id_UsersRepo

router = Router()

@router.message(Command("delete_group"))
async def send_message_to_group(message: Message):
    id_user = message.from_user.id
    if Id_UsersRepo.get_user(id_user) is None:
        if message.from_user.username is None:
            Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
        else:
            Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)

    for i in Id_UsersRepo.get_users():
        if str(i.id_group) == str(message.message_thread_id):
            Id_UsersRepo.update_group_user(i.telegram_id, None)

    TopicsRepo.delete_topic(message.message_thread_id)
    await message.reply("Чат удален")