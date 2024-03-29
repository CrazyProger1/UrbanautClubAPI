import peewee

from conf import settings
from utils.logging import logger
from utils.import_utils import import_module


def connect():
    logger.info('SQLite connection created')
    try:
        engine = import_module(settings.DATABASE.ENGINE)
    except ModuleNotFoundError:
        raise

    config = settings.DATABASE.PARAMS

    return engine(**config)


connection = connect()
