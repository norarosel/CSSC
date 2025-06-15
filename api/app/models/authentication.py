# -*- coding: utf-8 -*-
"""
    ADINMUGI

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from datetime import datetime

# Third-party app imports
from pydantic import BaseModel

# Imports from your apps
from app.config import settings


class AuthenticationSchema(BaseModel):
    username: str
    password: str
    date: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "username": settings.AUTH_USERNAME if settings.API_ENV == "develop" else "str",
                "password": settings.AUTH_PASSWORD if settings.API_ENV == "develop" else "str"
            }
        }


class AuthenticationResponse(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7ImtleSI6",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijp7ImtleSI6"
            }
        }
