# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import os
from datetime import timedelta

# Third-party app imports
from pydantic import BaseSettings
from fastapi_jwt import JwtAccessBearer
from fastapi_jwt import JwtRefreshBearer

# Imports from your apps


class BaseConfig(BaseSettings):
    API_ENV: str

    DB_HOSTNAME: str
    DB_PORT: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_AUTH_SOURCE: str

    AUTH_USERNAME: str
    AUTH_PASSWORD: str

    JWT_SECRET_KEY: bytes

    ROOT_PATH: str = ""

    def DB_URI(self):
        return "mongodb://{}:{}@{}:{}/{}?authSource={}".format(
            self.DB_USERNAME, self.DB_PASSWORD, self.DB_HOSTNAME, self.DB_PORT, self.DB_NAME, self.DB_AUTH_SOURCE
        )

    class Config:
        if os.path.exists("develop.env"):
            env_file = "develop.env"


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    TESTING: bool = True
    API_PARAMS: dict = {
        "debug": True,
        "docs_url": "/"
    }

    class Config:
        if os.path.exists("develop.env"):
            env_file = "develop.env"


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    TESTING: bool = False
    API_PARAMS: dict = {
        "debug": False,
        "redoc_url": "/"
    }

    class Config:
        if os.path.exists("production.env"):
            env_file = "production.env"


if os.environ.get("API_ENV", "develop") == "production":
    settings = ProductionConfig()
else:
    settings = DevelopmentConfig()


# Read access token from bearer header and cookie (bearer priority)
access_security = JwtAccessBearer(
    secret_key=settings.JWT_SECRET_KEY.decode("utf-8"),
    auto_error=True,
    access_expires_delta=timedelta(hours=1)
)
# Read refresh token from bearer header only
refresh_security = JwtRefreshBearer(
    secret_key=settings.JWT_SECRET_KEY.decode("utf-8"),
    auto_error=True
)
