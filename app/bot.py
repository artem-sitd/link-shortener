from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import asyncio
from ..settings import telegram_api_key
import re
from urls import create_unique_short_url

# Инициализация бота и диспетчера
bot = Bot(token=telegram_api_key)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # Протокол (http, https, ftp)
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Домен
    r'localhost|'  # Локальный хост
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IP-адрес
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
    r'(?::\d+)?'  # Порт (необязательно)
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_valid_url(url: str) -> bool:
    return re.match(URL_REGEX, url) is not None


# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне длинную ссылку, и я сделаю её короткой.")


# Основной хэндлер для сокращения ссылки
@dp.message_handler()
async def shorten_url(message: types.Message):
    original_url = message.text

    if not is_valid_url(original_url):
        await message.answer("Это не похоже на ссылку! Пожалуйста, отправьте действительный URL.")
        return

    short_url = await create_unique_short_url(original_url)

    await message.reply(f"Ваша короткая ссылка: https://short.ly/{short_url}")


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
