from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.repo import TopicsRepo, Id_UsersRepo
from config import Config
from database.repo import Id_UsersRepo
import os

router = Router()

@router.message(Command("choose_user_group"))
async def start(message: Message):
    id_user = message.from_user.id
    if Id_UsersRepo.get_user(id_user) is None:
        if message.from_user.username is None:
            Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
        else:
            Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)
    builder = InlineKeyboardBuilder()
    if message.reply_to_message is None:
        await message.reply("Ответьте на сообщение пользователя, чтобы перенаправлять его сообщения в группу")
    else:
        m = message.reply_to_message.text
        print(m)
        for i in TopicsRepo.get_topics():
            callback = f'{m[m.find('id: ') + 4:m.find('):\n')]} {i.id_topic}'
            builder.row(types.InlineKeyboardButton(text=i.name_topic, callback_data=callback))

        keyboard = builder.as_markup()

        if keyboard.inline_keyboard:
            await message.reply("Выберите группу", reply_markup=keyboard)
        else:
            await message.reply("Группы еще не добавлены")

@router.callback_query()
async def callback_handler(call: types.CallbackQuery):
    user_id, id_topic = call.data.split()
    while user_id.isdigit() == False:
        if user_id[0].isdigit() == False:
            user_id = user_id[1:]
        if user_id[-1].isdigit() == False:
            user_id = user_id[:-1]
    Id_UsersRepo.update_group_user(user_id, id_topic)
    if Id_UsersRepo.get_user_name(user_id) is None:
        await Config.bot.send_message(chat_id=os.environ.get("ID_MAIN_GROUP"), text=f'Пользователь {Id_UsersRepo.get_user(user_id).username} перешел в группу {TopicsRepo.get_topic(id_topic).name_topic}')
    else:
        await Config.bot.send_message(chat_id=os.environ.get("ID_MAIN_GROUP"), text=f'Пользователь {Id_UsersRepo.get_user(user_id).name_in_chat} перешел в группу {TopicsRepo.get_topic(id_topic).name_topic}')