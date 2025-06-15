# -*- coding: utf-8 -*-
"""
    ontology_responses.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party app imports
from pydantic import BaseModel

# Imports from your apps
from app.models.examples.ontology_schema import GET_ONTOLOGY_CLASSES


class GetOntologyClasses(BaseModel):

    class Config:
        schema_extra = {
            "example": GET_ONTOLOGY_CLASSES,
        }
