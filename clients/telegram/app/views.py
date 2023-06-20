import aiogram
from tbf.view import View
from tbf.models import *
from aiogram import types
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

    async def send_all_objects(self, user: TelegramUser):
        for obj in await AbandonedObjectAPIManager.list_paginated():
            obj: AbandonedObject
            states = {
                'd': 'dangerous',
                'b': 'bad',
                'a': 'average',
                'g': 'good',
                'n': 'novelty'
            }
            location: AbandonedObjectLocation = obj.location
            coordinates: Coordinates = location.coordinates
            address: Address = location.address
            await self._sender.send_message(user, f'''
<b>{aiogram.utils.markdown.quote_html(obj.name)}</b>

<i>Description:</i> {aiogram.utils.markdown.quote_html(obj.description)}
<i>Category:</i> {obj.category}
<i>State:</i> {states[obj.state]}
<i>Address:</i> {address.country}, {address.city}, {address.street}, {address.street_number}
<i>Coordinates:</i> {coordinates.latitude}x{coordinates.longitude}
''')

    async def on_button_pressed(self, keyboard: ReplyKeyboard, *args, button: str, user: TelegramUser, **kwargs):
        if 'back' in button:
            await self.back(user)

        if 'all' in button:
            await self.send_all_objects(user)
