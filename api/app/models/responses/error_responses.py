# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from pydantic import BaseModel

# Third-party app imports
from fastapi import HTTPException, status
from functools import singledispatch

# Imports from your apps


class ErrorResponseModel(BaseModel):
    code: int
    description: str
    message: str


@singledispatch
def ErrorResponse(description):
    raise NotImplementedError("Not implemented")


@ErrorResponse.register
def _(description: str = "", code: int = status.HTTP_400_BAD_REQUEST, message: str = ""):
    detail = {"code": code, "error": description, "message": message}
    raise HTTPException(status_code=code, detail=detail)


@ErrorResponse.register
def _(description: ErrorResponseModel):
    detail = description.dict()
    raise HTTPException(status_code=description.code, detail=detail)


class ErrorResponses:

    @classmethod
    def NotFound(cls, raise_error: bool = True, message: str = "item", replace_message: bool = False) -> dict:
        response_model = ErrorResponseModel(
            code=status.HTTP_404_NOT_FOUND,
            description="Item not found",
            message=f"Requested {message} not found in database" if not replace_message else message
        )
        return cls.__error_response(response_model, raise_error)

    @classmethod
    def Unauthorized(cls, raise_error: bool = True) -> dict:
        response_model = ErrorResponseModel(
            code=status.HTTP_401_UNAUTHORIZED,
            description="Unauthorized",
            message="Credentials are wrong"
        )
        return cls.__error_response(response_model, raise_error)

    @classmethod
    def ItemExists(cls, raise_error: bool = True, message: str = "Item") -> dict:
        response_model = ErrorResponseModel(
            code=status.HTTP_409_CONFLICT,
            description="Item already exists",
            message=f"{message} found in database"
        )
        return cls.__error_response(response_model, raise_error)

    @classmethod
    def Conflict(cls, raise_error: bool = True, message: str = "", description: str = "") -> dict:
        response_model = ErrorResponseModel(
            code=status.HTTP_409_CONFLICT,
            description=description or "Conflict",
            message=message or "Cannot modify the same condition more than once at the same time"
        )
        return cls.__error_response(response_model, raise_error)

    @classmethod
    def ValueError(cls, raise_error: bool = True, message: str = "", description: str = "") -> dict:
        response_model = ErrorResponseModel(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            description=description or "ValueError",
            message=message or "ValueError"
        )
        return cls.__error_response(response_model, raise_error)

    @classmethod
    def __error_response(cls, response_model: ErrorResponseModel, raise_error: bool = True):
        if raise_error:
            ErrorResponse(response_model)
        else:
            return cls.__response_documentation(response_model)

    @staticmethod
    def __response_documentation(error: ErrorResponseModel) -> dict:
        return {
            error.code: {
                "description": error.description,
                "content": {
                    "application/json": {
                        "example": {
                            "error": error.description,
                            "code": error.code,
                            "message": error.message
                        }
                    }
                }
            }
        }
