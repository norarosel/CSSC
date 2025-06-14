# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from typing import Tuple
from datetime import datetime
import requests

# Third-party src imports
import solara

# Imports from your apps
from src.config import settings
from src.models.PyObjectId import PyObjectId
from src.models.users import User
from src.models.resources import Resource


def authentication_header(access_token: str) -> dict:
    return {'Authorization': f"Bearer {access_token}"}


class AuthenticationProvider:
    @staticmethod
    def get_tokens(date: datetime | None = None) -> Tuple[str, str]:
        if date is None:
            date = datetime.now()
        response = requests.post(
            f"{settings.API_HOST}/auth",
            json={
                "username": settings.AUTH_USERNAME,
                "password": settings.AUTH_PASSWORD,
                "date": date.isoformat()
            }
        )
        if response.status_code == 200:
            tokens = response.json()
            return tokens["access_token"], tokens["refresh_token"]
        else:
            solara.Error(label="Error de autenticación.")


class UsersProvider:
    @staticmethod
    def get_users() -> Tuple[bool, list[User] | str]:
        response = requests.get(f"{settings.API_HOST}/users")
        if response.status_code == 200 and len(users := [User(**user) for user in response.json()]):
            return True, users
        else:
            return False, "No se pudo obtener la lista de usuarios."

    @staticmethod
    def get_user(access_token: str, user_id: str) -> Tuple[bool, User | str]:
        response = requests.get(
            f"{settings.API_HOST}/user/{user_id}",
            headers=authentication_header(access_token)
        )
        if response.status_code == 200:
            user = response.json()
            return True, User(**user)
        else:
            return False, "No se pudo obtener el usuario seleccionado."


class ResourcesProvider:
    @staticmethod
    def get_resources(
            access_token: str,
            user_id: PyObjectId,
            resource_type: str,
            topics: list[str],
            target_groups: list[str],
            cancer_types: list[str]
    ) -> Tuple[bool, list[Resource] | str]:
        response = requests.get(
            f"{settings.API_HOST}/resources",
            params={
                "user_id": user_id,
                "resource_type": resource_type,
                "topics": topics,
                "target_group": target_groups,
                "cancer_type": cancer_types
            },
            headers=authentication_header(access_token)
        )
        if response.status_code == 200 and len(resources := [Resource(**resource) for resource in response.json()]):
            return True, resources
        else:
            return False, "No se pudieron obtener los recursos solicitados."

    @staticmethod
    def get_resource(
            access_token: str,
            resource_type: str,
            resource_id: str,
            user_id: str | None = None
    ) -> Tuple[bool, Resource | str]:
        response = requests.get(
            f"{settings.API_HOST}/resource",
            params={
                "resource_type": resource_type,
                "resource_id": resource_id,
                "user_id": user_id
            },
            headers=authentication_header(access_token)
        )
        if response.status_code == 200:
            resource = response.json()
            return True, Resource(**resource)
        else:
            return False, "No se pudo obtener el recurso solicitado."


class FeedbackProvider:
    @staticmethod
    def post_feedback(
            access_token: str,
            resource_id: str,
            user_id: str,
            resource_type: str,
            score: int
    ) -> Tuple[bool, None | str]:
        response = requests.post(
            f"{settings.API_HOST}/resource/{resource_id}/feedback",
            params={"user_id": user_id, "resource_type": resource_type, "score": score},
            headers=authentication_header(access_token)
        )
        if response.status_code == 200:
            return True, None
        else:
            return False, "Error al pasar feedback."

    @staticmethod
    def post_favorite(
            access_token: str,
            resource_id: str,
            user_id: str,
            resource_type: str,
            score: int
    ) -> Tuple[bool, None | str]:
        response = requests.post(
            f"{settings.API_HOST}/resource/{resource_id}/favourite",
            params={"user_id": user_id, "resource_type": resource_type, "score": score},
            headers=authentication_header(access_token)
        )
        if response.status_code == 200:
            return True, None
        else:
            return False, "Error al marcar como favorito."

    @staticmethod
    def post_view(
            access_token: str,
            resource_id: str,
            user_id: str,
            resource_type: str,
            elapsed_time: int,
            date: datetime
    ) -> Tuple[bool, None | str]:
        response = requests.post(
            f"{settings.API_HOST}/resource/{resource_id}/views",
            params={"user_id": user_id, "resource_type": resource_type, "elapsed_time": elapsed_time,
                    "date": date},
            headers=authentication_header(access_token)
        )
        if response.status_code == 200:
            return True, None
        else:
            return False, "Error al guardar visita."
