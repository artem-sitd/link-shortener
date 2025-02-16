import hashlib
import datetime
from database import collection, client, db
from settings import settings


# Функция для генерации хэша из оригинальной ссылки
def generate_hash(original_url: str):
    return hashlib.sha256(original_url.encode("utf-8")).hexdigest()[
           :8
           ]  # берем первые 8 символов хэша


# Функция для проверки наличия URL в базе
async def check_existing_url(original_url: str):
    print(f'collection: {collection}')
    print(f'client: {client}')
    print(f'db: {db}')
    existing_url = await collection.find_one({"original_url": original_url})
    return existing_url


# Функция для генерации уникального короткого URL
async def create_unique_short_url(original_url: str):
    # Проверяем, существует ли уже такой длинный URL в базе
    existing_url = await check_existing_url(original_url)
    if existing_url:
        # Если URL существует, возвращаем его короткую ссылку
        return existing_url["short_url"]

    # Если URL новый, генерируем новый короткий хэш
    short_hash = generate_hash(original_url)

    # и соединяем с нашим доменом
    short_url = f'{settings.main_domain}/s/{short_hash}'

    # создаем новый документ в монго с короткой, оригинальной ссылкой
    document = {
        "original_url": original_url,
        "short_url": short_url,
        "created_at": datetime.datetime.now(datetime.UTC),
    }
    await collection.insert_one(document)
    return short_url
