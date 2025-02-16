from motor.motor_asyncio import AsyncIOMotorClient
from settings import settings

# Подключаемся к MongoDB
client = AsyncIOMotorClient(settings.mongo_client)
db = client[settings.mongo_db_name]
collection = db[settings.mongo_collection_name]
