# -*- coding: utf-8 -*-
"""
    resources.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from datetime import datetime

# Third-party app imports
from fastapi import APIRouter, Depends, Query, Security
from fastapi_jwt import JwtAuthorizationCredentials

# Imports from your apps
from app.config import settings, access_security
from app.database import LikesProvider
from app.database import FavouritesProvider
from app.database import ResourcesProvider
from app.database import UsersProvider
from app.database.ViewsProvider import ViewsProvider
from app.models.PyObjectId import PyObjectId
from app.models.enums import ResourceType
from app.models.enums import Topic
from app.models.enums import TargetGroup
from app.models.enums import CancerType
from app.models.resources import Resource
from app.models.responses.crud_responses import ItemUpdated
from app.models.responses.error_responses import ErrorResponses
from app.utils.authentication import authorize_user


router = APIRouter(
    prefix="/resource",
    tags=["Resources"],
    dependencies=[Depends(authorize_user)] if settings.API_ENV == "production" else [],
    responses=ErrorResponses.Unauthorized(raise_error=False),
)


@router.get("", response_model=Resource)
async def get_resource(
        resource_type: ResourceType,
        resource_id: PyObjectId,
        user_id: PyObjectId | None = None
) -> Resource:
    doc = await ResourcesProvider(resource_type).find_one_and_update(resource_id, {"$inc": {"viewCount": 1}})
    if user_id:
        query = {"user_id": user_id, "resource_id": resource_id, "resource_type": resource_type.value}
        like = await LikesProvider.find_one(query)
        favourite = await FavouritesProvider.find_one(query)
        doc.like = like is not None
        doc.favourite = favourite is not None
    return doc


@router.get("s", response_model=list[Resource])
async def get_resources(
        *,
        user_id: PyObjectId | None = None,
        resource_type: ResourceType,
        topics: list[Topic] | None = Query(None),
        cancer_type: list[CancerType] | None = Query(None),
        target_group: list[TargetGroup] | None = Query(None),
        n_resources: int = 20
) -> list[Resource]:
    query = {"user_id": user_id, "topics": topics, "cancer_type": cancer_type, "target_group": target_group}
    docs = await ResourcesProvider(resource_type).find(query, length=n_resources)
    """
    states = [f"Q{x}" for x in range(1, 6)]
    username = "random"

    # Starting the self learning Recommendation system
    rs = RecommendationSystem(username=username, states=states)
    rs.load_data(username=username)

    # Sample state
    state_id = rs.sample_state(username=username)

    # Get the list of recommended products
    seg_products = rs.recommendation(username=username, state_id=state_id, n_products=10, epsilon=0.5)
    print(seg_products)

    # Initiate customer actions
    selected_item = CustomerActions.random_action(seg_products)
    print(f'[INFO] Item {selected_item} selected')

    # Update reward
    rs.update_reward(username, state_id, selected_item)
    """
    return docs


@router.post("/{resource_id}/view", response_model=ItemUpdated)
async def resource_view(*, resource_id: PyObjectId, resource_type: ResourceType, user_id: PyObjectId):
    await ResourcesProvider(resource_type).find_one_and_update(resource_id, {"$inc": {"viewCount": 1}})
    return ItemUpdated()


async def _feedback(
        provider,
        resource_id: PyObjectId,
        user_id: PyObjectId,
        resource_type: ResourceType,
        credentials: JwtAuthorizationCredentials,
        score: int = None,
        elapsed_time: int = None,
        date: datetime = None,

):
    # Check that user exists
    user_exists = await UsersProvider.find_one(user_id)
    if not user_exists:
        ErrorResponses.NotFound()
    # Check that resource exists
    resource_exists = await ResourcesProvider(resource_type).find_one(resource_id)
    if not resource_exists:
        ErrorResponses.NotFound()
    # Check if the like/favourite/view is stored or not
    if elapsed_time is not None and date is not None:
        doc = {
            "user_id": user_id,
            "resource_id": resource_id,
            "resource_type": resource_type,
            "elapsed time": elapsed_time,
            "date": date
        }
    else:
        doc = {"user_id": user_id, "resource_id": resource_id, "resource_type": resource_type}

    like_exists = await provider.find_one(doc)
    if score is None:
        if not like_exists:
            # doc["date"] = datetime.fromisoformat(credentials.subject["date"])
            await provider.insert_one(doc)
    else:
        # Delete/insert document
        if like_exists and score == 0:
            # doc["date"] = datetime.fromisoformat(credentials.subject["date"])
            await provider.delete(like_exists)
        elif not like_exists and score == 1:
            doc["date"] = datetime.fromisoformat(credentials.subject["date"])
            await provider.insert_one(doc)
    return ItemUpdated()


@router.post("/{resource_id}/feedback", response_model=ItemUpdated)
async def resource_feedback(
        *,
        resource_id: PyObjectId,
        user_id: PyObjectId,
        resource_type: ResourceType,
        score: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    return await _feedback(LikesProvider, resource_id, user_id, resource_type, credentials, score)


@router.post("/{resource_id}/favourite", response_model=ItemUpdated)
async def resource_favourite(
        *,
        resource_id: PyObjectId,
        user_id: PyObjectId,
        resource_type: ResourceType,
        score: int,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    return await _feedback(FavouritesProvider, resource_id, user_id, resource_type, credentials, score)


@router.post("/{resource_id}/views", response_model=ItemUpdated)
async def resource_views(
        *,
        resource_id: PyObjectId,
        user_id: PyObjectId,
        resource_type: ResourceType,
        elapsed_time: int,
        date: datetime,
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    return await _feedback(ViewsProvider, resource_id, user_id, resource_type, credentials, None, elapsed_time, date)
