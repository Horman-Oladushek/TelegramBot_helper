from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from help_def.add_new_user_to_db import add_new_user_to_bd

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    add_new_user_to_bd(message.from_user.id, message)
    print(message.chat.type)
    if message.chat.type == "private":
        await message.reply(
            "Здравствуйте! Техподдержка принимает текстовые сообщения, фотографии с подписями и без, видео и видеосообщения (кружки в телеграм).\nОпишите свою проблему")
        # id_user = message.from_user.id
        # member = await Config.bot.get_chat_member(chat_id=os.environ.get("ID_MAIN_GROUP"), user_id=id_user)
        # print(member.status)
