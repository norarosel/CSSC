# -*- coding: utf-8 -*-
"""
    resources.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
import time
from datetime import datetime
from functools import partial
import pandas as pd

# Third-party src imports
import solara
import re
import jwt

# Imports from your apps
from src import access_token, user, resource_type
from src.config import settings
from src.models.enums import ResourceType, Topic, CancerType, TargetGroup
from src.models.resources import Resource
from src.utils.request_providers import ResourcesProvider, UsersProvider
from src.components.feedback import user_feedback
from src.components.event_saver import see_more_event, login_event


# Store current resource type timer
start_time_type = None
start_time_pagination = None


def resource_type_event(user_id: str, resource_type: str):
    global start_time_type
    # Create a DataFrame for type selection event
    res_type = pd.DataFrame(columns=["user", "date", "elapsed_time", "type"])
    if start_time_type is not None:
        # Calculate elapsed time with that type selected
        end_time = time.time()
        elapsed_time = (end_time - start_time_type)
        # Store the recently selected types in the DataFrame
        df = pd.DataFrame([{
            "user": user_id,
            "date": datetime.now(),
            "elapsed_time": elapsed_time,
            "type": resource_type,
        }])
        # Insert new selections in the DataFrame
        res_type = pd.concat([res_type, df])
        # print(res_type)
    # New start time for next resource type
    start_time_type = time.time()


def pagination_event(user_id: str, resource_type: str, page_number: int):
    global start_time_pagination
    # Create a DataFrame for pagination event
    pagination = pd.DataFrame(columns=["user", "date", "type", "page", "elapsed time"])
    if start_time_pagination is not None:
        # Calculate elapsed time navigating in that page
        end_time = time.time()
        elapsed_time = (end_time - start_time_pagination)
        # Store the recently searched resources in the DataFrame
        df = pd.DataFrame([{
            "user": user_id,
            "date": datetime.now(),
            "type": resource_type,
            "page": page_number,
            "elapsed time": elapsed_time
        }])
        # Insert new resources in the DataFrame
        pagination = pd.concat([pagination, df])
        # print(pagination)
    # New start time for next page
    start_time_pagination = time.time()


# Link from ResourceCard redirects to ResourcePage
@solara.component
def resource_page(resource_id: str, resource_type: str, user_id: str):
    elapsed_time = solara.use_reactive(0)
    # Save time user enters see more card
    start_time_more = time.time()
    # Get selected resource from resource_id
    valid, resource = ResourcesProvider.get_resource(access_token.value, resource_type, resource_id, user_id)
    if not valid:
        solara.Error(resource)
        return
    # Display complete resource info
    # Replace &quot; with " " in the resource title
    title = re.sub(r'&quot;', '"', resource.title)
    with solara.Card(title=title):
        # Resource description
        solara.Markdown(resource.description)
        # Link to resource if exits
        if resource.url:
            html = f'<p><a href="{resource.url}" target="_blank">Link to resource</a></p>'
            solara.HTML(tag="div", unsafe_innerHTML=html)
        # Get rating and post it to the API
        user_feedback(resource_id, user_id, resource_type, resource)
    # Input time spent in the resource for demo data storage
    solara.SliderInt(
        "How much time did you spend on this resource? (Long: 90', Avg: 15', Short: 3')",
        value=elapsed_time, min=0, max=100
    )
    solara.Markdown(f"**Minutes: **: {elapsed_time.value}")
    # Go back button, stores data frame and makes a post in the api
    with solara.Link("/resources"):
        solara.Button(
            label="Go back",
            color="green",
            on_click=partial(see_more_event, user_id, resource_id, resource_type, start_time_more,
                             elapsed_time.value)
        )


# ResourcesRecommendation calls ResourceCard
@solara.component
def resource_card(resource: Resource, resource_type: str, user_id: str):
    # Replace &quot; with " " in the resource title
    title = re.sub(r'&quot;', '"', resource.title)
    with solara.Card(
            title=title,
            subtitle=f"Views: {resource.view_count} - Likes: {resource.like_count}",
            elevation=100
    ):
        solara.Markdown(resource.description[0:300])

        with solara.CardActions():
            with solara.Row(gap="20px"):
                # Get rating and post it to the API
                user_feedback(str(resource.id), user_id, resource_type, resource)
                with solara.Link(f"/resource/{str(resource.id)}/{resource_type}/{user_id}"):
                    solara.Button(label=">", color="blue")


# HomePage calls ResourcesRecommendation
@solara.component
def resources_recommendation(start_time_login):

    # Define current page number and page items
    all_resources = solara.use_reactive([])
    current_page = solara.use_reactive(0)
    n_items = 6
    # start_time_pagination = None

    selected_topics, all_topics = solara.use_reactive([]), [x for x in Topic]
    selected_cancer_types, all_cancer_types = solara.use_reactive([]), [x for x in CancerType]
    selected_target_groups, all_target_groups = solara.use_reactive([]), [x for x in TargetGroup]

    with solara.Card():
        # Get user's info
        valid, current_user = UsersProvider.get_user(access_token.value, str(user.value.id))
        # Error if no users found or render the selected user info
        if not valid:
            solara.Error(current_user)
            return
        # Display user's info
        solara.Info(
            f"Username: {current_user.username} - "
            f"Birth date: {current_user.birth_date} - "
            f"Sex: {current_user.gender} - "
            f"Cancer type: {current_user.cancer_type} - "
            f"Description: {current_user.description}"
        )
        # Get access token
        decoded_token = jwt.decode(access_token.value, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        # Get date from access token
        decoded_token_date = decoded_token.get("subject", {}).get("date", None)
        # Convert date to correct format
        decoded_token_date = datetime.strptime(decoded_token_date, "%Y-%m-%dT%H:%M:%S.%f")
        date_without_seconds = decoded_token_date.strftime("%Y-%m-%d %H:%M")
        # Display date
        solara.Info(f"Current date: {date_without_seconds}")
        # Select resource type
        solara.ToggleButtonsSingle(value=resource_type, values=[resource_types for resource_types in ResourceType],
                                   on_value=resource_type_event(str(user.value.id), resource_type.value))
        # Select resource topics
        solara.SelectMultiple("Topics", values=selected_topics, all_values=all_topics)

        # Select cancer type
        solara.SelectMultiple("Cancer type", values=selected_cancer_types, all_values=all_cancer_types)

        # Select target group
        solara.SelectMultiple("Target Group", values=selected_target_groups, all_values=all_target_groups)

        # Get strings that match the API from the selected topics
        def get_associated_enum_value(selected_, all_):
            associated_values = []
            for selected_string in selected_:
                for topic_enum in all_:
                    if topic_enum.value == selected_string:
                        associated_values.append(topic_enum.name)
                        break
            return associated_values

        topics = get_associated_enum_value(selected_topics.value, all_topics)
        target_groups = get_associated_enum_value(selected_target_groups.value, all_target_groups)
        cancer_types = get_associated_enum_value(selected_cancer_types.value, all_cancer_types)

        # Get selected resources
        valid, resources_ = ResourcesProvider.get_resources(
            access_token.value, user.value.id, resource_type.value, topics, target_groups, cancer_types
        )

        # Error if no resources found or render the recommended resources
        if not valid:
            solara.Error(resources_)
            all_resources.set([])
        else:
            all_resources.set(resources_)

        # Get resources filtered by title
        selected_resources = resources_search(all_resources)

        # Search bar for each resource selected
        if valid:
            # Get only this page's resources
            selected_resources_page = selected_resources[
                current_page.value * n_items:(current_page.value + 1) * n_items
            ]
        else:
            selected_resources = selected_resources_page = []

        # Display the resources
        with solara.GridFixed(columns=3):
            for res in selected_resources_page or []:
                resource_card(res, resource_type.value, str(user.value.id))

        # Function to navigate to the previous page
        def previous_page():
            pagination_event(str(user.value.id), resource_type.value, current_page.value)
            current_page.value -= 1

        # Function to navigate to the next page
        def next_page():
            pagination_event(str(user.value.id), resource_type.value, current_page.value)
            current_page.value += 1

        # Create navigation buttons
        with solara.Row(gap="10px", justify="space-around"):
            with solara.Link("/login"):
                solara.Button(
                    label="Log out",
                    color="red",
                    on_click=partial(login_event, str(user.value.id), start_time_login)
                )
            solara.Button(label="Previous page", on_click=previous_page, disabled=current_page.value == 0)
            solara.Button(
                label="Next page",
                on_click=next_page,
                disabled=current_page.value == (len(selected_resources) // n_items)
            )


def resources_search(all_resources) -> list[Resource]:
    # Set return variable
    ret = all_resources.value
    text = solara.use_reactive("Enter title")
    # Input resource's title
    solara.InputText(label="Find the resource you are looking for.", value=text, continuous_update=False)
    # Return if there are no resources
    if len(ret) < 1:
        return []
    # Compare input with resources
    filtered_resources = filter(
        lambda res: any(word.lower() in res.title.lower().split() for word in text.value.lower().split()),
        all_resources.value
    )
    # In case no matches are found
    if not any(filtered_resources) and text.value.strip() not in ["Enter title", "", None]:
        solara.Warning("No resources found. Please wait up to 45 seconds to see if we can find a match.")
        ret = []
    elif any(filtered_resources) and text.value.strip() not in ["Enter title", "", None]:
        # Get start time of the search
        # start_time_search = time.time()
        # Parameter for 100% match of the search
        score_1_count = 0
        # Calculate similarity scores based on the number of matching words
        scores = []
        for resource in filtered_resources:
            title_words = re.findall(r'[\w"]+|\([\w\s]+\)', resource.title.lower())
            input_words = re.findall(r'\w+', text.value.lower())
            matches = sum(word in title_words for word in input_words)
            # Check if all input words are present in the resource title
            if matches == len(input_words):
                score = 1.0  # Full match, similarity score is 1.0
                score_1_count += 1
            else:
                score = matches / len(input_words)
            # Similarity score
            scores.append((resource, score))
        # Sort the resources based on the similarity scores
        sorted_resources = sorted(scores, key=lambda x: x[1], reverse=True)
        # Set return variable
        ret = [resource for resource, _, in sorted_resources]
    # Return
    return ret
