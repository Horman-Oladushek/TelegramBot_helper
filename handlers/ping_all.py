from config import Config
from aiogram import Router
from aiogram.types import Message
from database.repo import Id_UsersRepo
from aiogram.filters import Command, CommandObject

config = Config()
router = Router()

@router.message(Command("ping_all"))
async def ping_all(message: Message, command: CommandObject):
    try:
        check_password: str = command.args
        if check_password[check_password.find('-p')+3:] == Config.password:
            users = Id_UsersRepo.get_users()
            for user in users:
                await config.bot.send_message(chat_id=user.telegram_id, text=message.text[message.text.find('/ping_all')+10:message.text.find("-p")])
        else:
            await message.reply("Неправильный пароль")
    except Exception as e:
        pass