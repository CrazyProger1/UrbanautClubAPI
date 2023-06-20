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
        self.subscribe(self.Event.MESSAGE, self.on_message)

    async def on_message(self, message: types.Message, *args, **kwargs):
        await message.reply(message.text)
