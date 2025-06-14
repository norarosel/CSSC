# -*- coding: utf-8 -*-
"""
    users.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports

# Third-party src imports
import solara
import itertools

# Imports from your apps
from src import user
from src.models.users import User
from src.utils.request_providers import UsersProvider


@solara.component
def SelectUser():
    # Get users
    valid, users = UsersProvider.get_users()
    # Error if not user found
    if not valid:
        solara.Error(users)
        return
    # Set guest user as default user
    default_user: User = [x for x in users if x.username == "Guest"][0]
    # Initialize local state
    selected_user, set_selected_user = solara.use_state(default_user.username)
    # Body
    with solara.Column():
        # Input widget to select the current user
        solara.Select(label="User", value=selected_user, values=[x.username for x in users], on_value=set_selected_user)
        # Get the selected user
        selected_user_ = next((x for x in users if x.username == selected_user))
        # Set global solara state value
        user.set(selected_user_)


def SelectDate(now):
    # Create lists
    day_numbers = list(range(1, 31))
    day_names = ["Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon"]
    days = list(zip(day_numbers, itertools.cycle(day_names)))
    # Create solara variables
    day, hour = solara.use_reactive(days[now.day - 1]), solara.use_reactive(now.hour)
    # Select date
    solara.Select("Day", value=day, values=days)
    solara.Select("Hour", value=hour, values=list(range(0, 24)))
    # Return values
    return day.value, hour.value
