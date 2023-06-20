from tbf.view import View
from aiogram import types
from .keyboards import MainKeyboard


class MainView(View):
    keyboard_classes = (
        MainKeyboard,
    )

    class Meta:
        default = True
        path = 'main'

    def __init__(self, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)

        keyboard = MainKeyboard()
        keyboard.subscribe(keyboard.Event.BUTTON_PRESSED, self.on_search_objects)

    async def on_search_objects(self, keyboard, *args, button, **kwargs):
        print(keyboard, button, 'YEEA')
