from aiogram.types import Message
from aiogram import F, filters
from aiogram import Router
from bot import Config
import os

config = Config()
router = Router()

@router.message(F.reply_to_message)
async def reply_handler(message: Message):
    m = message.reply_to_message.text
    if m.find('id: ') != -1:
        id_user = m[m.find('id: ')+4:m.find('):\n')]
        print(id_user)
        await config.bot.send_message(chat_id=id_user, text=message.text)
        await message.reply(f"Ответ отправлен!")
    elif 'Ответ отправлен!' in m or 'Ожидайте ответа' in m:
        await message.reply('Возможно вы ответили на системное сообщение, повторите попытку отвечая не на системное сообщение')
    else:
        text = message.text
        id_user = message.from_user.id

        if message.from_user.username is None:
            text_to_group = f'Пользователь {message.from_user.full_name} (id: {id_user}):\n{text}'
        else:
            text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\nОтвет на:\n{message.reply_to_message.text}\n\nСообщение:\n{text}'
        await config.bot.send_message(
            chat_id=os.environ.get("ID_GROUP"),
            text=text_to_group
        )

        await config.bot.send_message(chat_id=id_user, text="Ожидайте ответа")