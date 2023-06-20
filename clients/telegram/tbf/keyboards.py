import functools

from enum import Enum
from utils import cls_utils, events
from .models import Language, TelegramUser
from .ui import UIObject
from .translator import _


class Keyboard(UIObject):
    button_keys: tuple[str] = (

    )

    class Meta:
        caption_key: str = ''
        autoshow: bool = False
        autohide: bool = False

    class Event(Enum):
        INITIALIZE = 1
        DESTROY = 2
        SHOW = 3
        HIDE = 4
        BUTTON_PRESSED = 5

    @functools.cache
    def get_markup(self, language: Language):
        raise NotImplementedError

    @functools.cache
    def get_caption(self, language: Language):
        try:
            return _(self.Meta.caption_key, language=language)
        except AttributeError:
            raise AttributeError('Meta.caption_key not specified')


class ReplyKeyboard(Keyboard):
    def get_markup(self, language: Language):
        pass
