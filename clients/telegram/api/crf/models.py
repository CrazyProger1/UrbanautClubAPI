import peewee
from database.database import db


class Model(peewee.Model):
    class Meta:
        database = db
