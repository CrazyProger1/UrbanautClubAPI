from aiogram import types
from tbf.translator import _
from tbf.view import View
from tbf.models import *

from .keyboards import *
from .services import *
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

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        if 'search_objects' in button:
            await self.next(user=user, view=SearchObjectsView)
        elif 'add_object' in button:
            pass


class SearchObjectsView(View):
    keyboard_classes = (
        SearchObjectsKeyboard,
    )

    class Meta:
        default = True
        path = 'main.search'

    def __init__(self, *args, **kwargs):
        super(SearchObjectsView, self).__init__(*args, **kwargs)
        SearchObjectsKeyboard().subscribe(MainKeyboard.Event.BUTTON_PRESSED, self.on_button_pressed)

    async def send_all_objects(self, user: TelegramUser):
        for obj in await get_all_objects(user=user):
            await self.sender.send_object(
                user=user,
                obj=obj
            )

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        if 'all' in button:
            await self.send_all_objects(user=user)
        elif 'back' in button:
            await self.back(user=user)
