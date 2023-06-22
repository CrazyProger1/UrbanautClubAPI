from conf import settings
from tbf.bot import Bot
from tbf.translator import Translator
from .views import *
from .models import *
from tbf.middlewares import *
from database.database import connection
from utils import filesystem, config
from utils.logging import logger
from tbf.models import *


class App(Bot):

    def __init__(self):
        super(App, self).__init__()

        self.subscribe(self.Event.INITIALIZE, self.initialize)
        self.subscribe(self.Event.DESTROY, self.destroy)

    def load_languages(self):
        for lang_folder in filesystem.iter_files(settings.L18N.LOCALE_FOLDER):
            if not lang_folder.is_dir() or len(lang_folder.name) != 2:
                continue

            data = config.JSONConfig.load(lang_folder / '.lang')
            Language.get_or_create(
                full_name=data.full_name,
                short_name=data.short_name,
            )
        logger.info('Loaded default languages')

    def initialize_db(self):
        connection.create_tables(Model.__subclasses__())
        self.load_languages()

    def initialize(self):
        self.initialize_db()
        Translator(settings.L18N.BOT_DOMAIN)

    def destroy(self):
        pass
