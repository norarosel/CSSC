# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party src imports
import solara
from src.models.resources import Resource

# Imports from your app
from src import access_token
from src.utils.request_providers import FeedbackProvider
from src.components.event_saver import like_event


def user_feedback(resource_id: str, user_id: str, resource_type: str, resource: Resource):
    # Set solara like value
    like, set_like = solara.use_state(resource.like)
    favorite, set_favorite = solara.use_state(resource.favourite)

    solara.Checkbox(label="Like", value=like, on_value=set_like)
    solara.Checkbox(label="Favorite", value=favorite, on_value=set_favorite)

    if like != resource.like:
        resource.like = like
        like_event(user_id, resource_id, resource_type, like)
        FeedbackProvider.post_feedback(access_token.value, resource_id, user_id, resource_type, int(like))
    if favorite != resource.favourite:
        resource.favourite = favorite
        FeedbackProvider.post_favorite(access_token.value, resource_id, user_id, resource_type, int(favorite))
