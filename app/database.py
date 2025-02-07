from motor.motor_asyncio import AsyncIOMotorClient
from ..settings import mongo_client, mongo_db_name, mongo_collection_name

# Подключаемся к MongoDB
client = AsyncIOMotorClient(mongo_client)
db = client[mongo_db_name]
collection = db[mongo_collection_name]
