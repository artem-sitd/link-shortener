from dotenv import load_dotenv
import os

load_dotenv()
telegram_api_key = os.getenv('telegram_api_key')
mongo_client = os.getenv('mongo_client')
mongo_db_name = os.getenv('db_name')
mongo_collection_name=os.getenv('mongo_collection_name')
