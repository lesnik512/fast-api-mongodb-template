from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


mongo_client = AsyncIOMotorClient(settings.MONGO_DETAILS)
database = getattr(mongo_client, settings.MONGO_DB_NAME)


async def drop_database() -> None:
    await mongo_client.drop_database(settings.MONGO_DB_NAME)
