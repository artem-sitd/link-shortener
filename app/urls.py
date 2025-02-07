import hashlib
from datetime import datetime
from database import collection


# Функция для генерации хэша из оригинальной ссылки
def generate_hash(original_url: str):
    return hashlib.sha256(original_url.encode("utf-8")).hexdigest()[
        :8
    ]  # берем первые 8 символов хэша


# Функция для проверки наличия URL в базе
async def check_existing_url(original_url: str):
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
    while True:
        short_hash = generate_hash(original_url)

        # Проверяем, существует ли уже такой короткий URL в базе данных
        existing_short_url = await collection.find_one({"short_url": short_hash})

        if not existing_short_url:
            # Если хэш уникален, сохраняем его в базе данных
            document = {
                "original_url": original_url,
                "short_url": short_hash,
                "created_at": datetime.utcnow(),
            }
            await collection.insert_one(document)
            return short_hash

        # Если такой короткий URL уже существует, генерируем новый
        original_url = original_url + str(
            datetime.utcnow()
        )  # модификация URL для создания уникального хэша
