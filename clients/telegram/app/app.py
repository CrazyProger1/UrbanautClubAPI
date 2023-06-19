from tbf.bot import Bot
from .views import *
from .middlewares import *
from .models import *
from database.database import connection


class App(Bot):

    def initialize_db(self):
        connection.create_tables(Model.__subclasses__())

    def initialize(self):
        self.initialize_db()

    def destroy(self):
        pass
