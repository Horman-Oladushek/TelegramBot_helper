from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
from help_def.add_new_user_to_db import add_new_user_to_bd

router = Router()

# class GetNameUser(StatesGroup):
#     organization = State()
#     name = State()

@router.message(Command("start"))
async def start(message: Message): #, state: FSMContext):
    add_new_user_to_bd(message.from_user.id, message)
    print(message.chat.type)
    if message.chat.type == "private":
        await message.reply( #'Здравствуйте! Напишите свою организацию')
        # await state.set_state(GetNameUser.organization)
            "Здравствуйте! Техподдержка принимает текстовые сообщения, фотографии с подписями и без, видео и видеосообщения (кружки в телеграм).\nОпишите свою проблему")
        # id_user = message.from_user.id
        # member = await Config.bot.get_chat_member(chat_id=os.environ.get("ID_MAIN_GROUP"), user_id=id_user)
        # print(member.status)

# @router.message(GetNameUser.organization)
# async def