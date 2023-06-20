import peewee
from database.model import Model
from conf import settings
from .limits import *


class TelegramUser(Model):
    id = peewee.IntegerField(primary_key=True)
    username = peewee.CharField(USERNAME_LENGTH)
    first_name = peewee.CharField(FIRSTNAME_LENGTH)
    last_name = peewee.CharField(LASTNAME_LENGTH, null=True)

    def is_admin(self):
        return self.id == settings.BOT.ADMIN
