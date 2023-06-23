import aiogram
from tbf.translator import _
from tbf.view import View
from tbf.models import *
from aiogram import types
from .keyboards import *
from .managers import AbandonedObjectAPIManager, AbandonedObjectCategoryAPIManager
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

        self.kb = MainKeyboard()
        self.kb.subscribe(self.kb.Event.BUTTON_PRESSED, self.on_button_pressed)

    async def on_button_pressed(self, keyboard: ReplyKeyboard, *args, button: str, user: TelegramUser, **kwargs):
        if 'search_objects' in button:
            await self.next(user, SearchObjectsView)


class SearchObjectsView(View):
    keyboard_classes = (
        SearchObjectsKeyboard,
    )

    class Meta:
        default = False
        path = 'main.search'

    def __init__(self, *args, **kwargs):
        super(SearchObjectsView, self).__init__(*args, **kwargs)
        self.kb = SearchObjectsKeyboard()
        self.kb.subscribe(self.kb.Event.BUTTON_PRESSED, self.on_button_pressed)

    async def on_button_pressed(self, keyboard: ReplyKeyboard, *, button: str, user: TelegramUser, **kwargs):
        if 'all' in button:
            await self.next(user, AllObjectsView)
        elif 'back' in button:
            await self.back(user)


class AllObjectsView(View):
    keyboard_classes = (
        AllObjectsNavKeyboard,
    )

    class Meta:
        default = False
        path = 'main.search.all'

    def __init__(self, *args, **kwargs):
        super(AllObjectsView, self).__init__(*args, **kwargs)
        self.kb = AllObjectsNavKeyboard()
        self.kb.subscribe(self.kb.Event.BUTTON_PRESSED, self.on_button_pressed)
        self.subscribe(self.Event.INITIALIZE, self.on_initialize)

    async def send_object(self, user: TelegramUser, obj: AbandonedObject):
        await self.sender.send_message(
            user,
            _(
                'contents.objects.object_form',
                user
            ).format(
                name=obj.name,
                desc=obj.description,
                category=_(f'contents.objects.categories.{obj.category}', user, default=obj.category),
                state=_(f'contents.objects.states.{obj.state}', user),
                address=None,
                latitude=obj.location.coordinates.latitude,
                longitude=obj.location.coordinates.longitude
            )

        )

    async def send_all_objects(self, user: TelegramUser):
        for obj in await AbandonedObjectAPIManager.list_paginated():
            await self.send_object(user, obj)

    async def on_initialize(self, user: TelegramUser):
        await self.send_all_objects(user)

    async def on_button_pressed(self, keyboard: ReplyKeyboard, *, button: str, user: TelegramUser, **kwargs):
        if 'back' in button:
            await self.back(user)
