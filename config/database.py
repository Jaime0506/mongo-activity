# database.py
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from config.config import settings

_client: Optional[AsyncIOMotorClient] = None

async def connect_to_mongo():
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.mongo_uri)

async def close_mongo_connection():
    global _client
    if _client:
        _client.close()
        _client = None

def get_db():
    if _client is None:
        raise RuntimeError("Mongo client not initialized. Call connect_to_mongo() on startup.")
    return _client[settings.MONGODB_DB]

def get_collection(name: str) -> AsyncIOMotorCollection:
    return get_db()[name]

def get_cars_collection() -> AsyncIOMotorCollection:
    # usa la collection definida en .env
    return get_collection(settings.MONGODB_COLLECTION_CARS)
