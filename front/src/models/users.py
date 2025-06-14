# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from datetime import datetime
from typing import Self

# Third-party src imports
from pydantic import Field

# Imports from your apps
from src.models.CustomBaseModel import CustomBaseModel
from src.models.PyObjectId import PyObjectId


class User(CustomBaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    birth_date: datetime = Field(..., alias="birthDate")
    gender: str
    cancer_type: str = Field(..., alias="cancerType")
    description: str
    days_seen: list[int] = Field([], alias="daysSeen")

    @classmethod
    def empty_user(cls) -> Self:
        cls.id = PyObjectId()
        cls.username = ""
        cls.birth_date = datetime.now()
        cls.gender = "H"
        cls.cancer_type = "breast"
        cls.description = "Guest user"
        cls.days_seen = []
        return cls


class UserSchemaIn(User):
    pass


class UserSchemaOut(User):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
