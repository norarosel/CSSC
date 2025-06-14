# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party src imports
import numpy as np
from pydantic import Field, validator, HttpUrl

# Imports from your apps
from src.models.CustomBaseModel import CustomBaseModel
from src.models.PyObjectId import PyObjectId


class Resource(CustomBaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    view_count: int | float = Field(..., alias="viewCount")
    like_count: int | float = Field(..., alias="likeCount")
    segment: str
    like: bool = False
    favourite: bool = False
    url: HttpUrl | None = None

    @validator('view_count', 'like_count')
    def validate_numeric_fields(cls, v):
        if np.isnan(v):
            v = 0
        elif isinstance(v, float):
            v = int(v)
        return v
