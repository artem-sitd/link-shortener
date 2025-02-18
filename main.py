from aiogram import types
from settings import settings
from aiohttp import web
from app.bot import dp, bot
import asyncio
from app.database import collection


# здесь же прописать ручку для приема короткой ссылки для дальнейшего редиректа на имеющийся полный url
# если такой короткой ссылки не найдено, тогда перевести на страницу заглушку "такой ссылки не существует"
async def redirect(request):
    # Парсим hash ссылки
    hash = request.match_info['hash']
    print(f'redirect: {hash}')

    # Ищем в базе данных
    link_data = await collection.find_one({"hash": hash})

    if not link_data:
        return web.Response(text="Ссылка не найдена", status=404)

    return web.HTTPFound(link_data["original_url"])  # Редирект на оригинальный сайт


# прием вебхуков
async def handle_webhook(request):
    print('message from webhook')
    update = await request.json()
    await dp.feed_update(bot, types.Update(**update))
    return web.Response()


async def index_page(request):
    return web.Response(
        text='<h1>This is test page. Hello!</h1>',
        content_type='text/html')


async def main():
    try:
        print('start web application aiohttp')
        # Запускаем веб-сервер для приема вебхуков
        app = web.Application()

        # ручка для приема вебхук от телеграма
        app.router.add_post(settings.WEBHOOK_PATH, handle_webhook)

        # ручка для редиректов
        app.router.add_get('/s/{hash}', redirect)

        # просто заглушка
        app.router.add_get('/', index_page)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        await site.start()

        # Устанавливаем вебхук
        print("set webhooks")
        await bot.set_webhook(settings.WEBHOOK_URL)

        # Бесконечный цикл для поддержания работы сервера
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        # Обработка остановки сервера
        pass
    finally:
        # Корректное завершение работы
        print('close session, storage, runner')
        await bot.session.close()  # Закрываем сессию бота
        await dp.storage.close()  # Закрываем хранилище диспетчера
        await runner.cleanup()  # Останавливаем веб-сервер


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Сервер остановлен.")
