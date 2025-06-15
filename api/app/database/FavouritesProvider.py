# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party app imports

# Imports from your apps
from app.database.DataProvider import DataProvider


class FavouritesProvider(DataProvider):
    collection = DataProvider.db["favourites"]
