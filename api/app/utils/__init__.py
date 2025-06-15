# -*- coding: utf-8 -*-
"""

    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from datetime import datetime, date
from http import HTTPStatus

# Third-party app imports
from operator import itemgetter
import bson.errors
from bson.objectid import ObjectId
from fastapi import HTTPException
from typing import Any

# Imports from your apps


def ids_to_string(doc: Any):
    if isinstance(doc, dict):
        for key, value in doc.items():
            doc[key] = ids_to_string(value)
    elif isinstance(doc, list):
        doc = list(map(ids_to_string, doc))
    elif isinstance(doc, ObjectId):
        doc = str(doc)
    return doc


def string_to_id(doc: Any):
    def _convert_string_to_id(_doc: dict):
        for key, value in _doc.items():
            if isinstance(value, str) and '_id' in key:
                _doc[key] = ObjectId(value)
            elif not isinstance(value, str):
                string_to_id(value)
        return _doc

    if isinstance(doc, dict):
        _convert_string_to_id(doc)
    elif isinstance(doc, list):
        doc = list(map(string_to_id, doc))
    elif isinstance(doc, str):
        doc = ObjectId(doc)
    return doc


def convert_ids(data: Any):
    try:
        if isinstance(data, list):
            data = list(map(convert_ids, data))
        elif isinstance(data, dict):
            _convert_dict_ids(data)
        elif isinstance(data, str) and data is not None:
            data = ObjectId(data)
        return data
    except bson.errors.InvalidId as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


def _convert_dict_ids(x: dict):
    for key, value in x.items():
        if "_id" in key and value is not None:
            x[key] = ObjectId(value)
        elif isinstance(value, dict):
            _convert_dict_ids(value)
        elif isinstance(value, list):
            convert_ids(value)


def convert_id(str_id: str) -> ObjectId:
    return ObjectId(str_id)


def convert_date(date_: date) -> datetime:
    return datetime(date_.year, date_.month, date_.day)


def remove_null_ids(cursor: list) -> list:
    ids = list(map(itemgetter('_id'), cursor))
    if (idx := ids.index(None) if None in ids else -1) >= 0:
        del cursor[idx]
    return cursor
