import logging

from utils.config import JSONConfig, ENVConfig
from aiogram import types

FILES = {
    'ENV_CONFIG_FILE': 'env/local.env',
}

env_conf = ENVConfig.load(FILES['ENV_CONFIG_FILE'])

DEBUG = True

APP = {
    'NAME': 'Urbanaut Club',
    'VERSION': '0.0.2'
}

LOGGING = {
    'FILE': 'app.log',
    'FILEMODE': 'a',
    'LEVEL': logging.DEBUG if DEBUG else logging.INFO,
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'PRINT_LOG': DEBUG
}

BOT = {
    'TOKEN': env_conf.TOKEN,
    'ADMIN': int(env_conf.ADMIN) if env_conf.ADMIN else 0,
    'ROUTER_CLASS': 'tbf.router.Router',
    'SENDER_CLASS': 'app.sender.Sender'
}

DATABASE = {
    'ENGINE': env_conf.DB_ENGINE,
    'PARAMS': {
        'database': env_conf.DB_FILE
    },
    'AUTHENTICATOR_CLASS': 'app.database.authenticator.Authenticator'
}

L18N = {
    'LOCALE_FOLDER': 'resources/languages',
    'BOT_DOMAIN': 'bot',
    'UPDATE_TRANSLATIONS': False
}

SUPPORT = {
    'TELEGRAM': 'crazyproger1'
}

COMMAND = {
    'PREFIX': '/',
    'REGEXP': fr'^\/\w+',
    'PARSER_CLASS': 'app.bot.types.Parser'
}

MESSAGES = {
    'PARSE_MODE': types.ParseMode.HTML
}
