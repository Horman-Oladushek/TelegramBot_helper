import time
import asyncio
import os
from aiogram import Router, Bot, Dispatcher
from handlers import bot_start, answer_to_user, take_all_messages, ping_all
from config import Config

config = Config()
router = Router()



async def main():
    bot = Bot(token=os.environ.get("TOKEN"))
    dp = Dispatcher()
    dp.include_routers(
        bot_start.router,
        answer_to_user.router,
        ping_all.router,
        take_all_messages.router
    )

    await bot.send_message(
        chat_id=os.environ.get("ID_GROUP"),
        text=f'Скрипт тех поддержки запущен в данном чате {time.strftime("%H:%M:%S %Y-%m-%d", time.localtime())}'
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    print('start', time.strftime("%H:%M:%S %Y-%m-%d", time.localtime()))
    asyncio.run(main())