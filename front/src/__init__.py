# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party src imports
import solara

# Imports from your apps
from src.models.enums import ResourceType
from src.models.users import User


# Global state variables
user = solara.reactive(User.empty_user())
resource_type = solara.reactive(ResourceType.video)
access_token = solara.reactive("")
