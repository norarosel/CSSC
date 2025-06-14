# -*- coding: utf-8 -*-
"""
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import time
from datetime import datetime
from functools import partial

# Third-party src imports
import solara

# Imports from your apps
from src import user
from src.utils.request_providers import AuthenticationProvider
from src.components.users import SelectUser, SelectDate
from src.components.resources import resources_recommendation, resource_page
from src import access_token

# Current date
now = datetime.now()


# START
@solara.component
def home_page():
    with solara.Row(gap="10px", justify="space-around"):
        with solara.Column(gap="10px"):
            with solara.Card(title="CANCER SURVIVOR SMART CARD DEMO"):
                solara.Image("images/vicom-logo.jpeg")
            with solara.Link("/login"):
                solara.Button(label="Start trial", color="blue")


# Login page
@solara.component
def login_page():
    def authenticate_user(current_date: datetime):
        access_token_, _ = AuthenticationProvider.get_tokens(current_date)
        access_token.set(access_token_)
    # Select user
    SelectUser()
    # Select day and hour
    day, hour = SelectDate(now)
    # Login
    with solara.Link("/resources"):
        # Show user description
        solara.Info(user.value.description)
        # Show days seen by user
        solara.Info(f"Days seen: {str(sorted(user.value.days_seen))}")
        solara.Button(
            label=f"Login as '{user.value.username}' at '{day}/{now.month}/{now.year}-{hour}:00'",
            color="green",
            on_click=partial(authenticate_user, now.replace(hour=hour, day=int(day[0])))
        )


# HomePage
@solara.component
def resource_list():
    # Save login event
    start_time_login = time.time()

    """Title"""
    with solara.AppBar():
        solara.Title("Home")

    """Body"""
    # Select resource
    resources_recommendation(start_time_login)


# Define URL, routes
routes = [
    solara.Route(path="/", component=home_page, label="Home Page"),
    solara.Route(path="login", component=login_page, label="Login"),
    solara.Route(path="resources", component=resource_list, label="Resources List"),
    solara.Route(path="resource", component=resource_page, label="Resource Page")
]
