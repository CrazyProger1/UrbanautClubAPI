import aiogram

from tbf.view import View
from aiogram import types
from .models import *


class MainView(View):
    class Meta:
        default = True
        path = 'main'

    def __init__(self, *args, **kwargs):
        super(MainView, self).__init__(*args, **kwargs)
        self.subscribe(self.Event.MESSAGE, self.on_message)

    async def on_message(self, *args, **kwargs):
        print(args, kwargs)
