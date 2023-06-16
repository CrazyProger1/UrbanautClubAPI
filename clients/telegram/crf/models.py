import peewee
from crf.database import db


class Model(peewee.Model):
    class Meta:
        database = db
