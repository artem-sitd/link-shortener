from aiogram import Bot
from aiogram.types import ParseMode
from aiogram.utils.executor import start_webhook
from ..settings import telegram_api_key, WEBHOOK_HOST, WEBHOOK_PATH, WEBHOOK_URL

bot = Bot(token=telegram_api_key)


# Функция для обработки стартового запроса
async def on_start(msg):
    await msg.answer("Bot is online.")


# Основная функция для настройки вебхука
async def on_start(msg):
    await msg.answer("Bot is online.")


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=WEBHOOK_PATH, on_start=on_start)
