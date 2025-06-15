# -*- coding: utf-8 -*-
"""
    users.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party app imports
from fastapi import APIRouter, Depends

# Imports from your apps
from app.config import settings
from app.models.PyObjectId import PyObjectId
from app.database.UsersProvider import UsersProvider
from app.models.responses.crud_responses import ItemCreated, ItemDeleted
from app.models.responses.error_responses import ErrorResponses
from app.models.user import UserSchemaIn
from app.models.user import UserSchemaOut
from app.utils.authentication import authorize_user


router = APIRouter(
    prefix="/user",
    tags=["Users"],
    responses=ErrorResponses.Unauthorized(raise_error=False),
)


@router.post(
    "",
    response_model=ItemCreated,
    dependencies=[Depends(authorize_user)] if settings.API_ENV == "production" else []
)
async def create_user(params: UserSchemaIn) -> ItemCreated:
    user_id = await UsersProvider.insert_one(params)
    return ItemCreated(detail=f"User created: {user_id}")


@router.get(
    "/{user_id}",
    response_model=UserSchemaOut,
    dependencies=[Depends(authorize_user)] if settings.API_ENV == "production" else []
)
async def get_user(user_id: PyObjectId) -> UserSchemaOut:
    doc = await UsersProvider.find_one(user_id)
    return doc


@router.get("s", response_model=list[UserSchemaOut])
async def get_users() -> list[UserSchemaOut]:
    doc = await UsersProvider.find()
    return doc


@router.delete(
    "/{user_id",
    response_model=ItemDeleted,
    dependencies=[Depends(authorize_user)] if settings.API_ENV == "production" else []
)
async def delete_user(user_id: PyObjectId) -> ItemDeleted:
    await UsersProvider.delete(user_id)
    return ItemDeleted(detail=f"User deleted: {user_id}")
