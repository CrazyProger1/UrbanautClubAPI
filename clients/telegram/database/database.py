import peewee


def get_database():
    return peewee.SqliteDatabase('app.db')


db = database = get_database()
