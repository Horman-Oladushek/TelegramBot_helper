from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.repo import Id_UsersRepo

router = Router()

@router.message(Command("help"))
async def start(message: Message):
    id_user = message.from_user.id
    if Id_UsersRepo.get_user(id_user) is None:
        if message.from_user.username is None:
            Id_UsersRepo.add_user(id_user, message.from_user.full_name, id_group=None)
        else:
            Id_UsersRepo.add_user(id_user, f'@{message.from_user.username}', id_group=None)

    await message.reply('Список команд:\n'
                        '/start - Запуск бота (использовать только в лс)\n'
                        '/help - Список команд доступных для использования\n'
                        '/add_group - Добавление группы для пересылки сообщений от пользователей\n'
                        '/delete_group - Удаление группы для пересылки\n'
                        '/choose_user_group (+ответ на сообщение пользователя) - Выбор группы для пересылки сообщений\n'
                        '/name Имя - Изменить имя себе\n'
                        '/name Имя (+ответ на сообщение пользователя) - Изменить имя пользователя\n'
                        '/ping_all - Массовая рассылка всем пользователям бота\n')