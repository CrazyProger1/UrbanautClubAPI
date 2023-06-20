import functools

from enum import Enum
from utils import cls_utils, events


class Keyboard(events.EventChannel, metaclass=cls_utils.SingletonMeta):
    class Event(Enum):
        BUTTON_PRESSED = 1

    @functools.cache
    def get_markup(self, language):
        raise NotImplementedError

    