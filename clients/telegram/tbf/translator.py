import functools
from .models import TelegramUser, Language


@functools.cache
def _(key: str, user: TelegramUser = None, language: Language = None):
    return key
