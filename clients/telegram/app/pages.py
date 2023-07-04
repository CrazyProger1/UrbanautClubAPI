import aiogram

from aiogram import types
from enum import Enum
from tbf.translator import _
from tbf.page import Page
from tbf.models import *

from .keyboards import *
from .services import *
from .models import *
from .creation_state import ObjectCreationState
from .tasks import *


class BasePage(Page):
    class Meta:
        default = False
        path = 'base'

    async def check_back(self, user: TelegramUser, button: str):
        if 'back' in button:
            await self.back(user)

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        await self.check_back(user=user, button=button)


class MainPage(BasePage):
    object_classes = (
        MainKeyboard,
    )

    class Meta:
        default = True
        path = 'main'

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        if 'search_objects' in button:
            await self.next(user=user, page=SearchObjectsPage)
        elif 'add_object' in button:
            await self.next(user=user, page=AddObjectPage)


class SearchObjectsPage(BasePage):
    object_classes = (
        SearchObjectsKeyboard,
    )
    task_classes = (
        SendAllObjectsTask,
    )

    class Meta:
        default = False
        path = 'main.search'

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        await super(SearchObjectsPage, self).on_button_pressed(keyboard, button, user, **kwargs)
        if 'all' in button:
            await self.execute_task(user=user, task=SendAllObjectsTask)


class AddObjectPage(BasePage):
    object_classes = (
        AddObjectKeyboard,
        SelectObjectCategoryKeyboard,
        SelectObjectStateKeyboard,
        AddObjectConfirmationKeyboard
    )

    task_classes = (
        InputObjectName,
        InputObjectDescription,
        InputObjectCoordinates
    )

    class Meta:
        default = False
        path = 'main.add_object'

    async def on_initialize(self, user: TelegramUser):
        await self.execute_task(user=user, task=InputObjectName)

    async def on_task_done(self, task: Task, user: TelegramUser):
        tasks = self.get_tasks()
        task_idx = tasks.index(task)
        try:
            next_task = tasks[task_idx + 1]
            await self.execute_task(user=user, task=next_task)
        except IndexError:
            pass

        # async def on_initialize(self, user: TelegramUser):
    #     user.state.object_creation_state = getattr(user.state, 'object_creation_state', ObjectCreationState())
    #
    #     for task in self.task_classes:
    #         task().subscribe(task.Event.DONE, self.on_task_done)
    #
    #     await self.execute_task(user=user, task=InputObjectNameTask)
    #
    # async def on_task_done(self, task, *args, user: TelegramUser, **kwargs):
    #     self._current_task_index = self.task_classes.index(task.__class__)
    #
    #     try:
    #         next_task = self.task_classes[self._current_task_index + 1]
    #         await self.execute_task(user=user, task=next_task)
    #     except IndexError:
    #         pass

    # class Event(Enum):
    #     INITIALIZE = 1
    #     DESTROY = 2
    #     MESSAGE = 3
    #     COMMAND = 4
    #     CALLBACK = 5
    #     MEDIA = 6
    #     BUTTON_PRESSED = 7
    #
    # def __init__(self, *args, **kwargs):
    #     super(AddObjectView, self).__init__(*args, **kwargs)
    # self.senders = (
    #     self.send_input_name,
    #     self.send_input_description,
    #     self.send_categories,
    #     self.send_states,
    #     self.send_coordinates
    # )
    # self.tasks = (
    #     (self.Event.MESSAGE, self.on_name_entered),
    #     (self.Event.MESSAGE, self.on_description_entered),
    #     (self.Event.BUTTON_PRESSED, self.on_category_entered),
    #     (self.Event.BUTTON_PRESSED, self.on_state_entered),
    #     (self.Event.MESSAGE, self.on_coordinates_entered)
    # )

    # async def on_initialize(self, user: TelegramUser):
    #     for event, callback in self.tasks:
    #         self.add_async_task(event, callback)
    #
    #     user.state.object_creation_state = getattr(user.state, 'object_creation_state', ObjectCreationState())
    #     await self.next_step(user=user)
    #
    # async def cancel(self, user: TelegramUser):
    #     user.state.object_creation_state.reset()
    #     await self.back(user)
    #     self.clear_tasks()
    #
    # async def send_input_name(self, user: TelegramUser):
    #     await self.sender.send_translated(user, 'contents.objects.creation.name')
    #
    # async def send_input_description(self, user: TelegramUser):
    #     await self.sender.send_translated(user, 'contents.objects.creation.description')
    #
    # async def send_categories(self, user: TelegramUser):
    #     await SelectObjectCategoryKeyboard().show(user=user)
    #
    # async def send_states(self, user: TelegramUser):
    #     await SelectObjectStateKeyboard().show(user=user)
    #
    # async def send_coordinates(self, user: TelegramUser):
    #     await self.sender.send_translated(user, 'contents.objects.creation.coordinates')
    #
    # async def next_step(self, user: TelegramUser):
    #     await self.senders[self.task_pointer](user=user)
    #
    # async def on_name_entered(self, *args, user: TelegramUser, **kwargs):
    #     await self.next_step(user)
    #
    # async def on_description_entered(self, *args, user: TelegramUser, **kwargs):
    #     await self.next_step(user)
    #
    # async def on_category_entered(self, keyboard, button: str, user: TelegramUser, **kwargs):
    #     if isinstance(keyboard, SelectObjectCategoryKeyboard):
    #         await self.next_step(user)
    #
    # async def on_state_entered(self, keyboard, button: str, user: TelegramUser, **kwargs):
    #     if isinstance(keyboard, SelectObjectStateKeyboard):
    #         await self.next_step(user)
    #
    # async def on_coordinates_entered(self, *args, user: TelegramUser, **kwargs):
    #     print('COORDS!')
    #
    # async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
    #
    #     if isinstance(keyboard, ReplyKeyboard):
    #         if 'cancel' in button:
    #             await self.cancel(user)
    #         elif 'back' in button:
    #             self.switch_task(-1)
    #             await self.next_step(user)
    #     else:
    #         await self.async_publish(self.Event.BUTTON_PRESSED, keyboard=keyboard, button=button, user=user, **kwargs)
