import aiogram
from aiogram import types
from tbf.translator import _
from tbf.view import View
from tbf.models import *

from .keyboards import *
from .services import *
from .models import *
from .creation_state import ObjectCreationState


class BaseView(View):
    class Meta:
        default = False
        path = 'base'

    def __init__(self, *args, **kwargs):
        super(BaseView, self).__init__(*args, **kwargs)
        self.subscribe(self.Event.INITIALIZE, self.on_initialize)
        self.subscribe(self.Event.MESSAGE, self.on_message)

        for keyboard_cls in self.keyboard_classes:
            keyboard_cls().subscribe(keyboard_cls.Event.BUTTON_PRESSED, self.on_button_pressed)

    async def check_back(self, user: TelegramUser, button: str):
        if 'back' in button:
            await self.back(user)

    async def on_initialize(self, user: TelegramUser):
        pass

    async def on_message(self, *args, **kwargs):
        pass

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
            msg: types.Message = await self.sender.send_object(
                user=user,
                obj=obj
            )
            coords = obj.location.coordinates
            try:
                await self.sender.send_location(
                    user=user,
                    latitude=coords.latitude,
                    longitude=coords.longitude,
                    reply_to_message_id=msg.message_id
                )
            except aiogram.utils.exceptions.BadRequest:
                pass

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        await super(SearchObjectsView, self).on_button_pressed(keyboard, button, user, **kwargs)
        if 'all' in button:
            await self.send_all_objects(user=user)


class AddObjectView(BaseView):
    keyboard_classes = (
        AddObjectKeyboard,
        SelectObjectCategoryKeyboard,
        SelectObjectStateKeyboard
    )

    class Meta:
        default = False
        path = 'main.add_object'

    def __init__(self, *args, **kwargs):
        super(AddObjectView, self).__init__(*args, **kwargs)

    async def cancel(self, user: TelegramUser):
        user.state.object_creation_state.reset()
        await self.back(user)

    async def on_name_inputted(self, user: TelegramUser, state: ObjectCreationState, text: str):
        state.data['name'] = text

    async def on_desc_inputted(self, user: TelegramUser, state: ObjectCreationState, text: str):
        state.data['description'] = text

    async def on_category_selected(self, user: TelegramUser, state: ObjectCreationState, button: str):
        try:
            category_name = button.split('.')[-1]
            state.data['category'] = get_category_by_name(name=category_name)
        except IndexError:
            pass
        except AbandonedObjectCategory.DoesNotExist:
            pass

    async def on_state_selected(self, user: TelegramUser, state: ObjectCreationState, button: str):
        try:
            obj_state = button.split('.')[-1]

            if obj_state not in {'d', 'b', 'a', 'g', 'n'}:
                return

            state.data['state'] = obj_state
        except IndexError:
            pass

    async def on_initialize(self, user: TelegramUser):
        user.state.object_creation_state = getattr(user.state, 'object_creation_state', ObjectCreationState())
        await self.sender.send_translated(user, 'contents.objects.creation.name')

    async def on_message(self, message: types.Message, user: TelegramUser, **kwargs):
        state: ObjectCreationState = user.state.object_creation_state
        step = state.step

        match step:
            case 0:
                await self.on_name_inputted(user, state, message.text)
                await self.sender.send_translated(user, 'contents.objects.creation.description')
            case 1:
                await self.on_desc_inputted(user, state, message.text)
                await SelectObjectCategoryKeyboard().show(user=user)

        if step < 2:
            state.next_step()

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        if isinstance(keyboard, ReplyKeyboard):
            if 'cancel' in button:
                await self.cancel(user)
        else:
            state: ObjectCreationState = user.state.object_creation_state
            step = state.step

            match step:
                case 2:
                    await self.on_category_selected(user, state, button)
                    await SelectObjectCategoryKeyboard().hide(user=user)
                    await SelectObjectStateKeyboard().show(user=user)
                case 3:
                    await self.on_state_selected(user, state, button)
                    await SelectObjectStateKeyboard().hide(user=user)

            if 2 >= step < 4:
                state.next_step()
