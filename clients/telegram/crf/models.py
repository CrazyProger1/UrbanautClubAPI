import peewee
from database.database import connection


class Model(peewee.Model):
    class Meta:
        database = connection
