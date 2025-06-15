# -*- coding: utf-8 -*-
"""
    ADINMUGI

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

# Stdlib imports
from secrets import compare_digest

# Third-party apps imports
from fastapi import APIRouter, status
from fastapi import Security
from fastapi_jwt import JwtAuthorizationCredentials

# Imports from your apps
from app.config import access_security
from app.config import refresh_security
from app.config import settings
from app.models.responses.error_responses import ErrorResponses
from app.models.authentication import AuthenticationResponse
from app.models.authentication import AuthenticationSchema


router = APIRouter(
    prefix="",
    tags=["Authentication"],
    dependencies=[],
    responses=ErrorResponses.Unauthorized(raise_error=False),
)


@router.post("/auth", response_model=AuthenticationResponse, status_code=status.HTTP_200_OK)
async def authentication(auth: AuthenticationSchema) -> AuthenticationResponse:
    """ Auth endpoint """
    if compare_digest(auth.username, settings.AUTH_USERNAME) and compare_digest(auth.password, settings.AUTH_PASSWORD):
        subject = {
            "key": settings.JWT_SECRET_KEY.decode('utf-8'),
            "username": auth.username,
            "date": auth.date.isoformat()
        }
        access_token = access_security.create_access_token(subject=subject)
        refresh_token = refresh_security.create_refresh_token(subject=subject)
        return AuthenticationResponse(access_token=access_token, refresh_token=refresh_token)
    else:
        ErrorResponses.Unauthorized(raise_error=True)


@router.post("/refresh", response_model=AuthenticationResponse, status_code=status.HTTP_200_OK)
def refresh(credentials: JwtAuthorizationCredentials = Security(refresh_security)) -> AuthenticationResponse:
    # Update access/refresh tokens pair
    # We can customize expires_delta when creating
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject)
    return AuthenticationResponse(access_token=access_token, refresh_token=refresh_token)
