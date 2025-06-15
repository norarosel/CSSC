# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from logging.config import dictConfig

# Third-party app imports
from fastapi import FastAPI
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

# Imports from your apps
from app.config import settings
from app.config.logger import LogConfig, logger
from app.routers.authentication import router as auth_router
from app.routers.users import router as users_router
from app.routers.resources import router as resources_router

# Configure logger before FastAPI initialization
dictConfig(LogConfig().dict())

app = FastAPI(**settings.API_PARAMS)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(resources_router)


def custom_openapi():
    """Define custom openAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    # Edit routes to work behind a proxy
    routes = app.routes
    if settings.API_ENV == "production" or settings.API_ENV == "preproduction":
        route: Route
        for route in routes:
            if "doc" not in route.path and "json" not in route.path and route.path != "/":
                route.path_format = f"{settings.ROOT_PATH}/api{route.path_format}"
    # Get OpenAPI schema
    openapi_schema = get_openapi(
        title="CSSC API",
        version="0.1.0",
        description="",
        routes=routes
    )
    # Include Vicomtech logo
    openapi_schema["info"]["x-logo"] = {
        "url": "https://ametic.es/sites/default/files/vicomtech-brta_rgb1_0.png"
    }
    # Update OpenAPI schema
    app.openapi_schema = openapi_schema
    # Return OpenAPI schema
    return app.openapi_schema


app.openapi = custom_openapi

# Prevent CORS errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc):
    logger.error(f'\"{request.method} {request.url.path}\"\n{exc.detail}')
    return JSONResponse(content=jsonable_encoder(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {"detail": exc.errors(), "body": exc.body}
    logger.error(f'\"{request.method} {request.url.path}\"\n{errors}')
    return JSONResponse(content=jsonable_encoder(errors), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
