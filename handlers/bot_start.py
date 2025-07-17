from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from database.repo import Id_UsersRepo

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет! Тех поддержка принимает текстовые сообщения, фотографии и подписи к ним.\nОпишите свою проблему")
    id_user = message.from_user.id
    if Id_UsersRepo.get_user(id_user) is None:
        Id_UsersRepo.add_user(id_user, (f'@{message.from_user.username}' or message.from_user.full_name))
