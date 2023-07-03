from conf import settings
from tbf.bot import Bot
from tbf.translator import Translator
from tbf.middlewares import *

from .pages import *
from .tasks import *
from .database import initialize_db
from .sender import Sender


class App(Bot):

    def __init__(self):
        super(App, self).__init__()
        self.subscribe(self.Event.INITIALIZE, self.initialize)

    def initialize(self):
        initialize_db()
        Translator(settings.L18N.BOT_DOMAIN)
