from tbf.translator import _
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

        MainKeyboard().subscribe(MainKeyboard.Event.BUTTON_PRESSED, self.on_button_pressed)

    async def on_button_pressed(self, keyboard: ReplyKeyboard, *args, button: str, user: TelegramUser, **kwargs):
        if 'search_objects' in button:
            await self.next(user, SearchObjectView)
        elif 'add_object' in button:
            await self.next(user, AddObjectView)


class SearchObjectView(View):
    keyboard_classes = (
        SearchObjectsKeyboard,
    )

    class Meta:
        default = False
        path = 'main.search'

    def __init__(self, *args, **kwargs):
        super(SearchObjectView, self).__init__(*args, **kwargs)
        SearchObjectsKeyboard().subscribe(SearchObjectsKeyboard.Event.BUTTON_PRESSED, self.on_button_pressed)

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

        AllObjectsNavKeyboard().subscribe(AllObjectsNavKeyboard.Event.BUTTON_PRESSED, self.on_button_pressed)
        self.subscribe(self.Event.INITIALIZE, self.on_initialize)

    async def send_object(self, user: TelegramUser, obj: AbandonedObject):
        address = obj.location.address
        coordinates = obj.location.coordinates
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
                address=f'{address.country}, {address.region}, {address.city}, {address.street}, {address.street_number}',
                latitude=coordinates.latitude,
                longitude=coordinates.longitude
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


class AddObjectView(View):
    keyboard_classes = (
        AddObjectKeyboard,
        AddObjectConfirmationKeyboard
    )
    steps = [
        'contents.objects.creation.name',
        'contents.objects.creation.description',
        'category'
    ]

    class Meta:
        default = False
        path = 'main.add_object'

    def __init__(self, *args, **kwargs):
        super(AddObjectView, self).__init__(*args, **kwargs)
        self.subscribe(self.Event.INITIALIZE, self.on_initialize)
        AddObjectKeyboard().subscribe(AddObjectKeyboard.Event.BUTTON_PRESSED, self.on_button_pressed)
        AddObjectConfirmationKeyboard().subscribe(AddObjectConfirmationKeyboard.Event.BUTTON_PRESSED,
                                                  self.on_button_pressed)
        self.subscribe(self.Event.MESSAGE, self.on_message)

    async def on_initialize(self, user: TelegramUser):

        user.state.object_creation_buffer = {
            'step': 0
        }
        await self.next_step(user)

    async def ask_confirmation(self, user: TelegramUser):
        await AddObjectConfirmationKeyboard().show(user)

    async def next_step(self, user: TelegramUser):

        curr_step = user.state.object_creation_buffer['step']

        if curr_step == len(self.steps):
            return await self.ask_confirmation(user)

        await self.sender.send_message(
            user,
            _(
                self.steps[curr_step],
                user
            )
        )
        user.state.object_creation_buffer['step'] += 1

    async def prev_step(self, user: TelegramUser):
        if user.state.object_creation_buffer['step'] > 1:
            user.state.object_creation_buffer['step'] -= 2
            await self.next_step(user)

    async def on_message(self, message: types.Message, user: TelegramUser, **kwargs):

        step = user.state.object_creation_buffer['step']

        match step:
            case 1:
                user.state.object_creation_buffer['name'] = message.text
            case 2:
                user.state.object_creation_buffer['description'] = message.text
            case 3:
                user.state.object_creation_buffer['category'] = None

        await self.next_step(user)

    async def cancel(self, user: TelegramUser):
        user.state.object_creation_buffer = None
        await self.back(user)

    async def on_button_pressed(self, keyboard: ReplyKeyboard | InlineKeyboard, *, button: str, user: TelegramUser,
                                **kwargs):
        if isinstance(keyboard, ReplyKeyboard):
            if 'cancel' in button:
                await self.cancel(user)
            elif 'back' in button:
                await self.prev_step(user)
        else:
            if 'cancel' in button:
                await self.cancel(user)
            elif 'apply' in button:
                print('Object creation...')
