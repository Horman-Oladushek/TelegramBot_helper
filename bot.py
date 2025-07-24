import time
import asyncio
import os
from aiogram import Router, Bot, Dispatcher
from handlers import bot_start, answer_to_user, take_all_messages, ping_all, change_name, add_group, choose_user_group, help, del_group
from config import Config
from database.repo import TopicsRepo
from aiogram.types import BotCommand, BotCommandScopeChat

config = Config()
router = Router()

bot = Bot(token=os.environ.get("TOKEN"))


async def set_commands():
    group_commands = [
        BotCommand(command="add_group", description="Добавить группу"),
        BotCommand(command="delete_group", description="Удалить группу"),
        BotCommand(command="choose_user_group", description="Выбрать группу для пользователя"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="name", description="Изменить имя"),
        BotCommand(command="ping_all", description="Массовая рассылка"),
    ]
    await bot.set_my_commands(commands=group_commands, scope=BotCommandScopeChat(chat_id=os.environ.get("ID_MAIN_GROUP")))



async def main():
    await set_commands()
    dp = Dispatcher()
    dp.include_routers(
        bot_start.router,
        choose_user_group.router,
        help.router,
        del_group.router,
        add_group.router,
        change_name.router,
        ping_all.router,
        answer_to_user.router,
        take_all_messages.router
    )

    await bot.send_message(
        chat_id=os.environ.get("ID_MAIN_GROUP"),
        text=f'Скрипт тех поддержки запущен в данном чате {time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())}'
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    print('start', time.strftime("%H:%M:%S %Y-%m-%d", time.localtime()))
    asyncio.run(main())