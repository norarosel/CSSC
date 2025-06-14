# -*- coding: utf-8 -*-
"""
    ResourceType.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

# Stdlib imports
from enum import StrEnum

# Third-party src imports

# Imports from your apps


class ResourceType(StrEnum):
    video = "videos"
    podcast = "podcasts"
    news = "news"
