from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.mongo_uri)
db = client[settings.db_name]

users_collection = db.users
notes_collection = db.notes