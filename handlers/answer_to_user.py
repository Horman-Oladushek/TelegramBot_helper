from aiogram.types import Message
from aiogram import F
from aiogram import Router
from bot import Config
from help_def.del_message import delete_message_after_delay
from database.repo import Id_UsersRepo
import asyncio
import os

config = Config()
router = Router()

tech_words = ['Ответ отправлен!', 'Ожидайте ответа', 'Скрипт тех поддержки запущен в данном чате']

@router.message(F.reply_to_message)
async def reply_handler(message: Message):
    id_user = message.from_user.ud
    if Id_UsersRepo.get_user(id_user) is None:
        if message.from_user.username is None:
            Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
        else:
            Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)
    m = message.reply_to_message.text
    try:
        if m.find('id: ') != -1:
            id_user = m[m.find('id: ') + 4:m.find('):\n')]
            print(id_user)
            if Id_UsersRepo.get_user_name(message.from_user.id) is not None:
                await config.bot.send_message(chat_id=id_user, text=f'{Id_UsersRepo.get_user_name(message.from_user.id)} ответил:\n{message.text}')
            else:
                await config.bot.send_message(chat_id=id_user, text=f'{message.from_user.full_name} ответил:\n{message.text}')
            answer = await message.reply(f"Ответ отправлен!")
            await asyncio.create_task(delete_message_after_delay(os.environ.get("ID_MAIN_GROUP"), answer.message_id))
        elif 'Ответ отправлен!' in m or 'Ожидайте ответа' in m or 'Скрипт тех поддержки запущен в данном чате' in m:
            await message.reply(
                'Возможно вы ответили на системное сообщение, повторите попытку ответив на другое сообщение')
        else:
            text = message.text
            id_user = message.from_user.id

            if message.from_user.username is None:
                text_to_group = f'Пользователь {message.from_user.full_name} (id: {id_user}):\n{text}'
            else:
                text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\nОтвет на:\n{message.reply_to_message.text}\n\nСообщение:\n{text}'
            await config.bot.send_message(
                chat_id=os.environ.get("ID_MAIN_GROUP"),
                message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
                text=text_to_group
            )

            answer = await config.bot.send_message(chat_id=id_user, text="Ожидайте ответа")
            await asyncio.create_task(delete_message_after_delay(message.chat.id, answer.message_id))
    except Exception as e:
        pass