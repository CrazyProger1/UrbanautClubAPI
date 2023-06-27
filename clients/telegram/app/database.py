import asyncio
import aiohttp.client_exceptions
from utils.logging import logger
from utils import filesystem, config
from database.database import connection
from tbf.models import *
from .models import *
from .managers import AbandonedObjectCategoryAPIManager


async def load_categories():
    for category in await AbandonedObjectCategoryAPIManager.list_paginated():
        category: AbandonedObjectCategory
        try:
            category.save(force_insert=True)
        except peewee.IntegrityError:
            pass
    logger.info('Loaded categories')


async def load_cities():
    logger.info('Loaded cities')


async def load_countries():
    logger.info('Loaded countries')


def load_languages():
    for lang_folder in filesystem.iter_files(settings.L18N.LOCALE_FOLDER):
        if not lang_folder.is_dir() or len(lang_folder.name) != 2:
            continue

        data = config.JSONConfig.load(lang_folder / '.lang')
        Language.get_or_create(
            full_name=data.full_name,
            short_name=data.short_name,
        )
    logger.info('Loaded default languages')


def initialize_db():
    connection.create_tables(Model.__subclasses__())
    logger.info(f'Tables created: {Model.__subclasses__()}')

    load_languages()

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(load_categories())
        loop.run_until_complete(load_cities())
        loop.run_until_complete(load_countries())
    except aiohttp.client_exceptions.ClientConnectorError:
        pass


__all__ = [
    'initialize_db'
]
