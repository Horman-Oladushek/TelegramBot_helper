from config import Config
from aiogram import Router
from aiogram.types import Message
from database.repo import Id_UsersRepo
from aiogram.filters import Command
import os

config = Config()
router = Router()

@router.message(Command("ping_all"))
async def ping_all(message: Message):
    try:
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