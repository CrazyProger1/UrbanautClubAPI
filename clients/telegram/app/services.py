from tbf.models import TelegramUser
from .managers import AbandonedObjectAPIManager
from .models import City


async def get_all_objects(user: TelegramUser):
    return await AbandonedObjectAPIManager.list_paginated()


def get_city_by_id(pk: int) -> City:
    return City.get_by_id(pk)
