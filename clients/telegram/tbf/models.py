import functools
import peewee

from database.model import Model
from conf import settings
from .state import UserState, get_state
from .limits import *


class Language(Model):
    short_name = peewee.CharField(max_length=SHORT_LANG_NAME, primary_key=True)
    full_name = peewee.CharField(max_length=FULL_LANG_NAME)

    @staticmethod
    @functools.cache
    def get_default():
        return Language.get_or_create(short_name='en', full_name='English')[0]
        # return Languages.get_by_id('en')


class TelegramUser(Model):
    id = peewee.IntegerField(primary_key=True)
    username = peewee.CharField(USERNAME_LENGTH)
    first_name = peewee.CharField(FIRSTNAME_LENGTH)
    last_name = peewee.CharField(LASTNAME_LENGTH, null=True)
    language = peewee.ForeignKeyField(Language, on_delete='SET DEFAULT', default=Language.get_default)

    def __init__(self, *args, **kwargs):
        super(TelegramUser, self).__init__(*args, **kwargs)

    def is_admin(self):
        return self.id == settings.BOT.ADMIN

    @property
    def state(self):
        return get_state(self)
