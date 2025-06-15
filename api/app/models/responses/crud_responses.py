# -*- coding: utf-8 -*-
"""
    eHST

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import uuid

# Third-party app imports
from pydantic import BaseModel
from pydantic import create_model

# Imports from your apps


class NotFound(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Item not found."},
        }


class ItemCreated(BaseModel):
    detail: str = "Item created"

    class Config:
        schema_extra = {
            "example": {"detail": "Item created"},
        }


class ItemUpdated(BaseModel):
    detail: str = "Item updated"

    class Config:
        schema_extra = {
            "example": {"detail": "Item updated"},
        }


class ItemDeleted(BaseModel):
    detail: str = "Item deleted"

    class Config:
        schema_extra = {
            "example": {"detail": "Item deleted"},
        }


class ResponseModelTemplate(BaseModel):
    code: int = 200
    message: str

    @classmethod
    def add_fields(cls, **field_definitions):
        return create_model(uuid.uuid4().hex, __base__=cls, **field_definitions)
