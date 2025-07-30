from config import Config
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from database.repo import Id_UsersRepo
import os

config = Config()
router = Router()

@router.message(Command("ping_all"))
async def ping_all(message: Message):
    try:
        id_user = message.from_user.id
        if Id_UsersRepo.get_user(id_user) is None:
            if message.from_user.username is None:
                Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
            else:
                Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)

        member = await Config.bot.get_chat_member(chat_id=os.environ.get("ID_MAIN_GROUP"), user_id=message.from_user.id)
        if member.status != 'left':
            users = Id_UsersRepo.get_users()
            for user in users:
                try:
                    await config.bot.send_message(chat_id=user.telegram_id, text=message.text[message.text.find('/ping_all')+10:])
                except Exception as e:
                    pass
            await message.reply("Успешно!")

    except Exception as e:
        pass