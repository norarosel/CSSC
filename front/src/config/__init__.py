# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import os

# Third-party src imports
from pydantic import BaseSettings

# Imports from your apps


class BaseConfig(BaseSettings):
    ENV: str

    API_HOST: str

    AUTH_USERNAME: str
    AUTH_PASSWORD: str

    JWT_SECRET_KEY: str

    class Config:
        if os.path.exists("develop.env"):
            env_file = "develop.env"


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    TESTING: bool = True

    class Config:
        if os.path.exists("develop.env"):
            env_file = "develop.env"


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    TESTING: bool = False

    class Config:
        if os.path.exists("production.env"):
            env_file = "production.env"


if os.environ.get("API_ENV", "develop") == "production":
    settings = ProductionConfig()
else:
    settings = DevelopmentConfig()
