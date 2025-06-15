# -*- coding: utf-8 -*-
"""
    authentication.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

# Stdlib imports

# Third-party app imports
from fastapi import HTTPException
from fastapi import Security
from fastapi_jwt import JwtAuthorizationCredentials

# Imports from your apps
from app.config import access_security


async def authorize_user(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if not credentials:
        raise HTTPException(status_code=401, detail='Unauthorized')
