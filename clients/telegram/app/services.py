from tbf.models import TelegramUser
from .managers import AbandonedObjectAPIManager
from .models import *


async def get_all_objects(user: TelegramUser):
    return await AbandonedObjectAPIManager.list_paginated()


def get_city_by_id(pk: int, raise_exceptions=True) -> City:
    try:
        return City.get_by_id(pk)
    except Exception as e:
        if raise_exceptions:
            raise e


def get_category_by_name(name: str, raise_exceptions=True) -> AbandonedObjectCategory:
    try:
        return AbandonedObjectCategory.get_by_id(name)
    except Exception as e:
        if raise_exceptions:
            raise e


def get_country_by_name(name: str, raise_exceptions=True) -> Country:
    try:
        return Country.get(name=name)
    except Exception as e:
        if raise_exceptions:
            raise e
