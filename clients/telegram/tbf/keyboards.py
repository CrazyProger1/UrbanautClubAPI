import functools

from enum import Enum
from utils import cls_utils, events
from .models import Language
from .ui import UIObject


class Keyboard(UIObject):
    class Event(Enum):
        INITIALIZE = 1
        DESTROY = 2
        BUTTON_PRESSED = 3

    @functools.cache
    def get_markup(self, language: Language):
        raise NotImplementedError
