from aiogram import Bot, Dispatcher, types
from ..settings import telegram_api_key, WEBHOOK_PATH, WEBHOOK_URL
from aiogram.enums import ParseMode
from aiohttp import web
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=telegram_api_key, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())


async def handle_webhook(request):
    update = await request.json()
    await dp.feed_update(bot, types.Update(**update))
    return web.Response()


async def main():
    # Устанавливаем вебхук
    await bot.set_webhook(WEBHOOK_URL)

    # Запускаем веб-сервер для приема вебхуков
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 443)  # HTTPS-порт
    await site.start()


if __name__ == "__main__":
    asyncio.run(main())
