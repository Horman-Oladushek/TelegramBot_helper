import os
from dotenv import load_dotenv
from aiogram import Bot

class Config:
    load_dotenv()
    BOT_TOKEN = os.environ.get("TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Не удалось получить токен бота из переменной окружения TOKEN")
    bot = Bot(token=BOT_TOKEN)
    password = os.environ.get("PASSWORD")
