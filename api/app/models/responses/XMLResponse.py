# -*- coding: utf-8 -*-
"""
    XMLResponse.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

# Stdlib imports

# Third-party app imports
from fastapi import Response

# Imports from your apps


class XMLResponse(Response):
    media_type = "application/xml"
