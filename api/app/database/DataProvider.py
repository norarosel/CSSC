# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party app imports
from bson import ObjectId
import motor.motor_asyncio
from asyncio import get_event_loop

# Imports from your apps
from app.config import settings
from app.models.PyObjectId import PyObjectId
from app.models.responses.error_responses import ErrorResponses


class DataProvider:
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DB_URI())
    client.get_io_loop = get_event_loop
    db = client[settings.DB_NAME]
    collection = None

    @classmethod
    async def insert_one(cls, params: dict, check_if_exists: dict | None = None) -> ObjectId:
        if check_if_exists and (await cls.find_one(check_if_exists)):
            ErrorResponses.ItemExists()
        return (await cls.collection.insert_one(params)).inserted_id

    @classmethod
    async def find_one(cls, query: dict | str | ObjectId, project: dict | None = None) -> dict | None:
        if isinstance(query, str):
            query = {"_id": ObjectId(query)}
        elif isinstance(query, ObjectId):
            query = {"_id": query}
        doc = cls.collection.find_one(query) if project is None else cls.collection.find_one(query, project)
        return await doc

    @classmethod
    async def find(
        cls,
        query: dict | str | ObjectId | None = None,
        project: dict | None = None,
        length: int | None = None
    ) -> list:
        if query is None:
            query = {}
        if project is None:
            data = await cls.collection.find(query).to_list(length=length)
        else:
            data = await cls.collection.find(query, project).to_list(length=length)
        return data

    @classmethod
    async def update_one(cls, query: dict, new_values: dict) -> bool:
        return (await cls.collection.update_one(query, new_values)).modified_count > 0

    @classmethod
    async def find_and_update(cls, query: dict, new_values: dict, error_message: str = "item") -> dict:
        result = await cls.collection.update_many(query, {'$set': new_values})
        if result.modified_count == 0:
            ErrorResponses.NotFound(message=error_message, raise_error=True)
        result = await cls.collection.find_one(query)
        return result

    @classmethod
    async def find_one_and_update(cls, query: dict | PyObjectId, new_values: dict, error_message: str = "item") -> dict:
        if isinstance(query, (PyObjectId, ObjectId)):
            query = {"_id": query}
        result = await cls.collection.find_one_and_update(query, new_values)
        if result is None:
            ErrorResponses.NotFound(message=error_message, raise_error=True)
        result = await cls.collection.find_one(query)
        return result

    @classmethod
    async def delete(cls, query: dict | str | ObjectId) -> bool:
        if isinstance(query, str):
            query = {"_id": ObjectId(query)}
        elif isinstance(query, ObjectId):
            query = {"_id": query}
        return (await cls.collection.delete_many(query)).deleted_count > 0

    @classmethod
    async def aggregate(cls, aggregation: list[dict], collection_name: str | None = None) -> list:
        collection = cls.collection if collection_name is None else cls.db[collection_name]
        return await collection.aggregate(aggregation).to_list(length=None)
