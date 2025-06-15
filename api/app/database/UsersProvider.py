# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party app imports
from bson import ObjectId

# Imports from your apps
from app.database.DataProvider import DataProvider
from app.models.user import UserSchemaIn
from app.models.user import UserSchemaOut


class UsersProvider(DataProvider):
    collection = DataProvider.db["users"]

    @classmethod
    async def insert_one(cls, params: UserSchemaIn, check_if_exists: dict | None = None) -> ObjectId:
        if not isinstance(params, UserSchemaIn):
            raise ValueError("params must be a UserSchema")
        doc = await super().insert_one(params.dict())
        return doc

    @classmethod
    async def find_one(cls, query: dict | ObjectId | None, project: dict = None) -> UserSchemaOut:
        doc = await super().find_one(query, project)
        return UserSchemaOut(**doc)

    @classmethod
    async def find(
        cls,
        query: dict | str | ObjectId | None = None,
        project: dict | None = None,
        length: int | None = None
    ) -> list[UserSchemaOut]:
        docs = await super().find(query, project, length)
        return [UserSchemaOut(**doc) for doc in docs]
