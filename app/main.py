from aiogram import Bot, Dispatcher, types
from ..settings import telegram_api_key, WEBHOOK_PATH, WEBHOOK_URL
from aiogram.enums import ParseMode
from aiohttp import web
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from dotenv import load_dotenv
from pathlib import Path
from database import collection

bot = Bot(token=telegram_api_key, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())


# здесь же прописать ручку для приема короткой ссылки для дальнейшего редиректа на имеющийся полный url
# если такой короткой ссылки не найдено, тогда перевести на страницу заглушку "такой ссылки не существует"
async def redirect(request):
    # Получаем полный URL, по которому пришел запрос
    full_url = str(request.url)

    # Ищем в базе данных
    link_data = await collection.find_one({"short_url": full_url})

    if not link_data:
        return web.Response(text="Ссылка не найдена", status=404)

    return web.HTTPFound(link_data["original_url"])  # Редирект на оригинальный сайт


# прием вебхуков
async def handle_webhook(request):
    update = await request.json()
    await dp.feed_update(bot, types.Update(**update))
    return web.Response()


async def main():
    # Устанавливаем вебхук
    await bot.set_webhook(WEBHOOK_URL)

    # Запускаем веб-сервер для приема вебхуков
    app = web.Application()

    # ручка для приема вебхук от телеграма
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # ручка для редиректов
    app.router.add_get('/s/{hash}', redirect)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 443)  # HTTPS-порт
    await site.start()


if __name__ == "__main__":
    local = True
    env_file = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_file)
    asyncio.run(main())
