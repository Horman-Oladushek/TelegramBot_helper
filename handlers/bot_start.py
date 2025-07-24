from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from database.repo import Id_UsersRepo
from config import Config
import os

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.reply(
        "Здравствуйте! Техподдержка принимает текстовые сообщения, фотографии с подписями и без.\nОпишите свою проблему")
    id_user = message.from_user.id
    member = await Config.bot.get_chat_member(chat_id=os.environ.get("ID_MAIN_GROUP"), user_id=id_user)
    print(member.status)
    if Id_UsersRepo.get_user(id_user) is None:
        if message.from_user.username is None:
            Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
        else:
            Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)

