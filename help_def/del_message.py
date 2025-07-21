from config import Config
import asyncio


async def delete_message_after_delay(chat_id, message_id: int, delay: int = 5):
    await asyncio.sleep(delay)  # Задержка в секундах
    await Config.bot.delete_message(chat_id=chat_id, message_id=message_id)
