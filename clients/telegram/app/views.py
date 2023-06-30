from aiogram import types
from tbf.translator import _
from tbf.view import View
from tbf.models import *

from .keyboards import *
from .services import *
from .models import *


class BaseView(View):
    class Meta:
        default = False
        path = 'base'

    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        if len(self.keyboard_classes) > 0:
            self.keyboard_classes[0]().subscribe(MainKeyboard.Event.BUTTON_PRESSED, self.on_button_pressed)

    async def check_back(self, user: TelegramUser, button: str):
        if 'back' in button:
            await self.back(user)

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        await self.check_back(user=user, button=button)


class MainView(BaseView):
    keyboard_classes = (
        MainKeyboard,
    )

    class Meta:
        default = True
        path = 'main'

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        if 'search_objects' in button:
            await self.next(user=user, view=SearchObjectsView)
        elif 'add_object' in button:
            await self.next(user=user, view=AddObjectView)


class SearchObjectsView(BaseView):
    keyboard_classes = (
        SearchObjectsKeyboard,
    )

    class Meta:
        default = False
        path = 'main.search'

    async def send_all_objects(self, user: TelegramUser):
        for obj in await get_all_objects(user=user):
            await self.sender.send_object(
                user=user,
                obj=obj
            )

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        await super(SearchObjectsView, self).on_button_pressed(keyboard, button, user, **kwargs)
        if 'all' in button:
            await self.send_all_objects(user=user)


class AddObjectView(BaseView):
    keyboard_classes = (
        AddObjectKeyboard,
    )

    class Meta:
        default = False
        path = 'main.add_object'

    async def cancel(self, user: TelegramUser):
        await self.back(user)

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        if 'cancel' in button:
            await self.cancel(user)
