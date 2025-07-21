from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from database.repo import Id_UsersRepo
from help_def.del_message import delete_message_after_delay
import asyncio

router = Router()


@router.message(Command("name"))
async def start(message: Message):
    name = message.text[6:]
    if message.reply_to_message is None:
        Id_UsersRepo.update_name_user(message.from_user.id, name)
        answer = await message.reply("Ваше имя изменено")
        await asyncio.create_task(delete_message_after_delay(message.chat.id, answer.message_id))
    else:
        message_replyed = message.reply_to_message.text
        user_id = message_replyed[message_replyed.find('id: ') + 4:message_replyed.find('):')]
        Id_UsersRepo.update_name_user(user_id, name)
        answer = await message.reply(f"Имя пользователя {user_id} изменено")
        await asyncio.create_task(delete_message_after_delay(message.chat.id, answer.message_id))
