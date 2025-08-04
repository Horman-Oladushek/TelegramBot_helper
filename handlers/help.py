from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from help_def.add_new_user_to_db import add_new_user_to_bd
from config import Config
import os
router = Router()

@router.message(Command("help"))
async def start(message: Message):
    add_new_user_to_bd(message.from_user.id, message)
    if message.chat.type != 'private':
        await message.reply('Список команд:\n'
                            '/start - Запуск бота (использовать только в лс)\n'
                            '/help - Список команд доступных для использования\n'
                            '/add_group - Добавление группы для пересылки сообщений от пользователей\n'
                            '/delete_group - Удаление группы для пересылки\n'
                            '/choose_user_group (+ответ на сообщение пользователя) - Выбор группы для пересылки сообщений\n'
                            '/name Имя - Изменить имя себе\n'
                            '/name Имя (+ответ на сообщение пользователя) - Изменить имя пользователя\n'
                            '/ping_all - Массовая рассылка всем пользователям бота\n')
    else:
        await message.reply('Поддерживаются сообщения следующего типа:\n'
                            'Текстовые сообщения\n'
                            'Фотографии с подписями\n'
                            'Фотографии без подписей\n'
                            'Видео\n'
                            'Видеосообщения (кружки)\n\n'
                            'Стикеры, Гиф-сообщения, аудиосообщения НЕ поддерживаются')
