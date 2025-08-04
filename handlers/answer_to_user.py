from aiogram.types import Message
from aiogram import F, types
from aiogram import Router
from bot import Config
from help_def.del_message import delete_message_after_delay
from help_def.add_new_user_to_db import add_new_user_to_bd
from database.repo import Id_UsersRepo
import asyncio
import os

config = Config()
router = Router()


@router.message(F.reply_to_message)
async def reply_handler(message: Message):
    id_user = message.from_user.id
    #Шалости с бд
    add_new_user_to_bd(id_user, message)


    if message.reply_to_message.text is None:
        m = message.reply_to_message.caption
    else:
        m = message.reply_to_message.text
    #Проверка на системные сообщения
    if 'Ответ отправлен!' in m or 'Ожидайте ответа' in m or 'Скрипт тех поддержки запущен в данном чате' in m or 'Техподдержка принимает текстовые сообщения, фотографии с подписями и без, видео и видеосообщения' in m or 'Возможно вы ответили на системное сообщение, повторите попытку ответив на другое сообщение' in m:
        await message.reply('Возможно вы ответили на системное сообщение, повторите попытку ответив на другое сообщение')


    #Проверка чата
    if message.chat.type == 'private':
        flag_vlozh = False
        if message.text is not None:
            text = message.text
        else:
            flag_vlozh = True
            text = message.caption

        if message.reply_to_message.text is not None:
            answer_text = message.reply_to_message.text
        else:
            answer_text = message.reply_to_message.caption

        if message.reply_to_message.document is not None:
            flag_vlozh = True
            answer_text = f'Ответ на сообщение с файлом {message.reply_to_message.document.file_name}:\n{answer_text}'

        if Id_UsersRepo.get_user(id_user).name_in_chat is not None:
            text_to_group = f'{Id_UsersRepo.get_user(id_user).name_in_chat} (id: {id_user}):\nОтвет на:\n{answer_text}\n\nСообщение:\n{text}'
        elif message.from_user.username is None:
            text_to_group = f'Пользователь {message.from_user.full_name} (id: {id_user}):\nОтвет на:\n{answer_text}\n\nСообщение:\n{text}'
        else:
            text_to_group = f'Пользователь @{message.from_user.username} (id: {id_user}):\nОтвет на:\n{answer_text}\n\nСообщение:\n{text}'

        if flag_vlozh is True:

            if message.reply_to_message.photo is not None or message.reply_to_message.video is not None:
                media = []
                if message.reply_to_message.photo is not None:
                    media.append(types.InputMediaPhoto(media=message.reply_to_message.photo[-1].file_id, caption=text_to_group))  # message.reply_to_message.photo[-1].file_id
                    if message.photo is not None:
                        media.append(types.InputMediaPhoto(media=message.photo[-1].file_id))
                    else:
                        media.append(types.InputMediaVideo(media=message.video[-1].file_id))
                else:
                    media.append(types.InputMediaVideo(media=message.reply_to_message.video.file_id, caption=text_to_group))
                    if message.video is not None:
                        media.append(types.InputMediaVideo(media=message.video[-1].file_id))
                    else:
                        media.append(types.InputMediaPhoto(media=message.photo[-1].file_id))
                await config.bot.send_media_group(
                    chat_id=os.environ.get("ID_MAIN_GROUP"),
                    message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
                    media=media,
                )
            if message.reply_to_message.document is not None:

                await config.bot.send_document(
                    chat_id=os.environ.get("ID_MAIN_GROUP"),
                    message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None),
                    document=message.reply_to_message.document.file_id,
                    caption=text_to_group
                )

            if message.reply_to_message.video_note is not None:
                await message.answer("Просим прощения, ответы на видеосообщения не поддерживаются.\nОтветьте на другое сообщение или напишите без ответа.")
        if message.caption is not None:
            await config.bot.send_photo(chat_id=os.environ.get("ID_MAIN_GROUP"), message_thread_id=(Id_UsersRepo.get_user(id_user).id_group or None), photo=message.photo[-1].file_id, caption=text_to_group)
        answer = await config.bot.send_message(chat_id=id_user, text="Ожидайте ответа")
        await asyncio.create_task(delete_message_after_delay(message.chat.id, answer.message_id))
    try:
        if message.chat.type != 'private':
            if m.find('id: ') != -1:
                id_user = m[m.find('id: ') + 4:m.find('):\n')]
                if message.photo is not None:
                    if message.caption != None:
                        await config.bot.send_photo(chat_id=id_user, photo=message.photo[-1].file_id, caption=f'{Id_UsersRepo.get_user_name(message.from_user.id)} ответил:\n{message.caption}')
                    else:
                        await config.bot.send_photo(chat_id=id_user, photo=message.photo[-1].file_id, caption=f'{Id_UsersRepo.get_user_name(message.from_user.id)} ответил:')
                if message.video is not None:
                    if message.caption != None:
                        await config.bot.send_video(chat_id=id_user, video=message.video.file_id, caption=f'{Id_UsersRepo.get_user_name(message.from_user.id)} ответил:\n{message.caption}')
                    else:
                        await config.bot.send_video(chat_id=id_user, video=message.video.file_id, caption=f'{Id_UsersRepo.get_user_name(message.from_user.id)} ответил:')
                if message.document is not None:
                    if message.caption != None:
                        await config.bot.send_document(chat_id=id_user, document=message.document.file_id, caption=f'{Id_UsersRepo.get_user_name(message.from_user.id)} ответил:\n{message.caption}')
                    else:
                        await config.bot.send_document(chat_id=id_user, document=message.document.file_id, caption=f'{Id_UsersRepo.get_user_name(message.from_user.id)} ответил:')
                else:
                    if Id_UsersRepo.get_user_name(message.from_user.id) is not None:
                        await config.bot.send_message(chat_id=id_user, text=f'{Id_UsersRepo.get_user_name(message.from_user.id)} ответил:\n{message.text}')
                    else:
                        await config.bot.send_message(chat_id=id_user, text=f'{message.from_user.full_name} ответил:\n{message.text}')

                answer = await message.reply(f"Ответ отправлен!")
                await asyncio.create_task(delete_message_after_delay(os.environ.get("ID_MAIN_GROUP"), answer.message_id))
    except Exception as e:
        pass