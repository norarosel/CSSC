# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @author: Nora Rosel Zaballos - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from datetime import date, datetime, timezone

# Third-party src imports
from bson import ObjectId
from pydantic import BaseModel
from dateutil import tz

# Imports from your apps


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


def transform_to_utc_datetime(dt: datetime) -> datetime:
    return dt.astimezone(tz=timezone.utc)


def convert_date_to_datetime(dt: date) -> datetime:
    return datetime(dt.year, dt.month, dt.day)


def convert_date_to_europe_timezone(dt: datetime) -> str:
    if dt.tzinfo is None or dt.tzinfo.zone != "Europe/Madrid":
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Madrid')
        utc = dt.replace(tzinfo=from_zone)
        return str(utc.astimezone(to_zone))
    else:
        return str(dt)


def camel_to_snake(s: str) -> str:
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class CustomBaseModel(BaseModel):

    def validate_onto(cls, onto, onto_classes):
        pass

    def __getitem__(cls, arg):
        return getattr(cls, arg)

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        smart_union = True
        json_encoders = {
            ObjectId: str,
            # datetime: convert_date_to_europe_timezone
        }
