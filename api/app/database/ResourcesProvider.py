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
from app.models.PyObjectId import PyObjectId
from app.models.enums.ResourceType import ResourceType
from app.models.enums import Topic
from app.models.enums import CancerType
from app.models.enums import TargetGroup
from app.models.resources import Resource
from app.models.responses.error_responses import ErrorResponses


class ResourcesProvider(DataProvider):
    collection = DataProvider.db

    def __init__(self, resource_type: ResourceType):
        self.__class__.collection = self.db[resource_type]

    @classmethod
    async def find_one(cls, query: dict | ObjectId | None, project: dict = None) -> Resource:
        if (doc := await super().find_one(query, project)) is None:
            ErrorResponses.NotFound()
        return Resource(**doc)

    @classmethod
    async def find_one_and_update(
            cls,
            query: dict | PyObjectId,
            new_values: dict,
            error_message: str = "item"
    ) -> Resource:
        doc = await super().find_one_and_update(query, new_values, error_message)
        return Resource(**doc)

    @classmethod
    async def find(
        cls,
        query: dict | None = None,
        project: dict | None = None,
        length: int | None = None
    ) -> list[Resource]:
        if isinstance(query, dict):
            user_id: ObjectId = query["user_id"]
            topics: list[Topic] = query["topics"] if query.get("topics") else []
            cancer_type: list[CancerType] = query["cancer_type"] if query.get("cancer_type") else []
            target_group: list[TargetGroup] = query["target_group"] if query.get("target_group") else []
            aggregation = cls.__find(user_id, topics, cancer_type, target_group)
            docs = await super().aggregate(aggregation)
        else:
            docs = await super().find(query, project, length)
        return [Resource(**doc) for doc in docs]

    @classmethod
    async def update_reward(cls, resource_id: PyObjectId | ObjectId, user_id: ObjectId):
        await super().find_one_and_update(resource_id, {'$inc': {'viewCount': 1}})

    @staticmethod
    def __find(
            user_id: ObjectId,
            topics: list[Topic],
            cancer_type: list[CancerType],
            target_group: list[TargetGroup],
    ) -> list[dict]:
        pipeline = [
            {
                '$lookup': {
                    'from': 'likes',
                    'let': {'resource_id': '$_id'},
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {'$eq': ['$resource_id', '$$resource_id']},
                                        {'$eq': ['$user_id', user_id]}
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'like'
                }
            }, {
                '$lookup': {
                    'from': 'favourites',
                    'let': {'resource_id': '$_id'},
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {'$eq': ['$resource_id', '$$resource_id']},
                                        {'$eq': ['$user_id', user_id]}
                                    ]
                                }
                            }
                        }
                    ],
                    'as': 'favourite'
                }
            }, {
                '$set': {
                    'like': {'$gt': [{'$size': '$like'}, 0]},
                    'favourite': {'$gt': [{'$size': '$favourite'}, 0]}
                }
            }
        ]

        match_step = {}
        if topics:
            match_step['topics'] = {'$in': topics}
        if cancer_type and CancerType.all not in cancer_type:
            match_step['cancer_type'] = {'$in': cancer_type}
        if target_group:
            match_step['target_group'] = {'$in': target_group}
        if match_step:
            pipeline.insert(0, {'$match': match_step})
        return pipeline
