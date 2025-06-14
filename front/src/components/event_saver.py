# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from datetime import datetime, timedelta
import time

# Third-party src imports
import pandas as pd
import jwt

# import solara

# Imports from your apps
from src import access_token
from src.config import settings
from src.utils.request_providers import FeedbackProvider


# Hecho pero tienen que darle sí o sí al reset search
def search_event(user_id: str, sorted_resources, resource_type: str, score_1_count: int,
                 start_time_search: float, text):
    # Reset to default
    text.set("Enter title")
    # Create a DataFrame for search event
    search = pd.DataFrame(columns=["user", "date", "elapsed_time", "title", "type", "similarity score",
                                   "complete matches"])
    # Calculate elapsed time in the search
    end_time = time.time()
    elapsed_time = (end_time - start_time_search)
    # Store the recently searched resources in the DataFrame
    for resource, score in sorted_resources:
        df = pd.DataFrame([{
            "user": user_id,
            "date": datetime.now(),
            "elapsed_time": elapsed_time,
            "title": resource.title,
            "type": resource_type,
            "similarity score": score,
            "complete matches": score_1_count
        }])
        # Insert new resources in the DataFrame
        search = pd.concat([search, df])
    # print(search)


# Hecho pero le tienen que dar al log out
def login_event(user_id: str, start_time_login: float):
    # Create a DataFrame for login event
    login = pd.DataFrame(columns=["user", "date", "elapsed_time"])
    # Calculate elapsed time between login events
    end_time = time.time()
    elapsed_time = (end_time - start_time_login)
    # Store the recently logged-in Users in the DataFrame
    df = pd.DataFrame([{
        "user": user_id,
        "date": datetime.now(),
        "elapsed_time": elapsed_time,
    }])
    # Insert new logs in the DataFrame
    login = pd.concat([login, df])
    # print(login)


# Hecho en resources
# def resource_type_event(user_id: str, resource_type: str, start_time_type: float):
#     # Create a DataFrame for type selection event
#     res_type = pd.DataFrame(columns=["user", "date", "elapsed_time", "type"])
#     # Calculate elapsed time with that type selected
#     end_time = time.time()
#     elapsed_time = (end_time - start_time_type)
#     # Store the recently selected types in the DataFrame
#     df = pd.DataFrame([{
#         "user": user_id,
#         "date": datetime.now(),
#         "elapsed_time": elapsed_time,
#         "type": resource_type,
#     }])
#     # Insert new selections in the DataFrame
#     res_type = pd.concat([res_type, df])
#     # print(res_type)


# Hecho
def see_more_event(user_id: str, resource_id: str, resource_type: str,
                   start_time_more: float,
                   input_time: int):
    # Post in the API
    token_value = access_token.value.strip("'")

    # Decode the access token
    decoded_token = jwt.decode(token_value, settings.JWT_SECRET_KEY, algorithms=["HS256"])

    # Extract and return the date from the decoded token
    token_date = decoded_token.get("subject", {}).get("date", None)
    token_date = datetime.strptime(token_date, "%Y-%m-%dT%H:%M:%S.%f")

    # Extract the minutes from token_date and add input_time minutes
    updated_date = token_date + timedelta(minutes=input_time)
    # Save the updated date in the decoded token
    decoded_token["subject"]["date"] = updated_date.strftime("%Y-%m-%dT%H:%M:%S.%f")
    # Encode the updated and decoded token
    new_token = jwt.encode(decoded_token, settings.JWT_SECRET_KEY, algorithm="HS256")
    # Save updated access_token
    access_token.set(new_token)

    # Post view with updated_date
    FeedbackProvider.post_view(access_token.value, resource_id, user_id, resource_type, input_time, updated_date)

    # Create a DataFrame for see more event
    more = pd.DataFrame(columns=["user", "date", "elapsed_time", "resource_id", "type", "fake_time"])
    # Calculate elapsed time seeing more of a resource
    end_time = time.time()
    elapsed_time = (end_time - start_time_more)
    # Store the recently viewed resources in the DataFrame
    df = pd.DataFrame([{
        "user": user_id,
        "date": datetime.now(),
        "elapsed_time": elapsed_time,
        "resource_id": resource_id,
        "type": resource_type,
        "fake_time": input_time
    }])
    # Insert new views in the DataFrame
    more = pd.concat([more, df])
    # print(more)


def like_event(user_id: str, resource_id: str, resource_type: str, like_value: bool):
    # Post user like

    # Create a DataFrame for rating event
    rating = pd.DataFrame(columns=["user", "date", "resource_id", "type", "like"])
    # Store the recently searched resources in the DataFrame
    df = pd.DataFrame([{
        "user": user_id,
        "date": datetime.now(),
        "resource_id": resource_id,
        "type": resource_type,
        "like": like_value
    }])
    # Insert new resources in the DataFrame
    rating = pd.concat([rating, df])
    # print(rating)


# Hecho en resources, la primera página es la 0
# def pagination_event(user_id: str, resource_type: str, page_number: int, start_time_pagination):
#     # Create a DataFrame for pagination event
#     pagination = pd.DataFrame(columns=["user", "date", "type", "page", "elapsed time"])
#     if start_time_pagination is not None:
#         # Calculate elapsed time navigating in that page
#         end_time = time.time()
#         elapsed_time = (end_time - start_time_pagination)
#         # Store the recently searched resources in the DataFrame
#         df = pd.DataFrame([{
#             "user": user_id,
#             "date": datetime.now(),
#             "type": resource_type,
#             "page": page_number,
#             "elapsed time": elapsed_time
#         }])
#         # Insert new resources in the DataFrame
#         pagination = pd.concat([pagination, df])
#         # print(pagination)
#     # New start time for next page
#     start_time_pagination = time.time()
