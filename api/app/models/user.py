# -*- coding: utf-8 -*-
"""
    user.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from datetime import datetime

# Third-party app imports
from pydantic import Field

# Imports from your apps
from app.models.CustomBaseModel import CustomBaseModel
from app.models.PyObjectId import PyObjectId


class UserSchema(CustomBaseModel):
    username: str
    birth_date: datetime
    gender: str
    cancer_type: str
    description: str


class UserSchemaIn(UserSchema):
    pass


class UserSchemaOut(UserSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
