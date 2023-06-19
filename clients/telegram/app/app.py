from tbf.bot import Bot
from .views import *
from .middlewares import *
from .models import *
from database.database import connection


class App(Bot):

    def __init__(self):
        super(App, self).__init__()

        self.subscribe(self.Event.INITIALIZE, self.initialize)
        self.subscribe(self.Event.DESTROY, self.destroy)

    def initialize_db(self):
        connection.create_tables(Model.__subclasses__())

    def initialize(self):
        self.initialize_db()

    def destroy(self):
        pass
