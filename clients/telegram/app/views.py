from aiogram import types
from tbf.translator import _
from tbf.view import View
from tbf.models import *

from .keyboards import *
from .managers import AbandonedObjectAPIManager
from .models import *


class MainView(View):
    keyboard_classes = (
        MainKeyboard,
    )

    class Meta:
        default = True
        path = 'main'

    def __init__(self, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)
        MainKeyboard().subscribe(MainKeyboard.Event.BUTTON_PRESSED, self.on_button_pressed)

    async def on_button_pressed(self, *args, **kwargs):
        print(args, kwargs)
