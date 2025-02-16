import re
from urls import create_unique_short_url
from aiogram import types
from main import dp

URL_REGEX = re.compile(
    r"^(?:http|ftp)s?://"  # Протокол (http, https, ftp)
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]*[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # Домен
    r"localhost|"  # Локальный хост
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # IP-адрес
    r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # IPv6
    r"(?::\d+)?"  # Порт (необязательно)
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def is_valid_url(url: str) -> bool:
    return re.match(URL_REGEX, url) is not None


# Команда /start
@dp.message(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне длинную ссылку, и я сделаю её короткой.")


# Основной хэндлер для сокращения ссылки
@dp.message()
async def shorten_url(message: types.Message):
    original_url = message.text.strip()

    if not is_valid_url(original_url):
        await message.answer(
            "Это не похоже на ссылку! Пожалуйста, отправьте действительный URL."
        )
        return

    short_url = await create_unique_short_url(original_url)

    await message.reply(f"Ваша короткая ссылка: https://pqpq.pw/{short_url}")
