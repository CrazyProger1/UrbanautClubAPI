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

    )

    class Meta:
        default = False
        path = 'main.search'

    async def on_button_pressed(self, keyboard, button: str, user: TelegramUser, **kwargs):
        await super(SearchObjectsPage, self).on_button_pressed(keyboard, button, user, **kwargs)
        if 'all' in button:
            await self.next(user=user, page=AllObjectsPage)


class AllObjectsPage(BasePage):
    object_classes = (
        AllObjectsNavKeyboard,
    )
    task_classes = (
        SendAllObjectsTask,
    )

    class Meta:
        default = False
        path = 'main.search.all'

    async def on_initialize(self, user: TelegramUser):
        await self.execute_task(user=user, task=SendAllObjectsTask)


class AddObjectPage(BasePage):
    object_classes = (
        AddObjectKeyboard,
        SelectObjectCategoryKeyboard,
        SelectObjectStateKeyboard,
        CreateObjectConfirmationKeyboard
    )

    task_classes = (
        InputObjectName,
        InputObjectDescription,
        InputObjectCoordinates,
        SelectObjectCategoryTask,
        SelectObjectStateTask,
        ConfirmObjectCreationTask,
        CreateObjectTask
    )

    class Meta:
        default = False
        path = 'main.add_object'

    async def on_initialize(self, user: TelegramUser):
        user.state.ocs = ObjectCreationState()
        await self.execute_task(user=user, task=InputObjectName)

    async def on_task_done(self, task: Task, user: TelegramUser):
        tasks = self.get_tasks()
        task_idx = tasks.index(task)
        try:
            next_task = tasks[task_idx + 1]
            await self.execute_task(user=user, task=next_task)
        except IndexError:
            await self.back(user=user)

    async def prev_task(self, user: TelegramUser):
        tasks: tuple = self.get_tasks()
        task: Task = next(filter(lambda t: t.is_executing(user=user), tasks))

        task_idx = tasks.index(task)
        try:
            if task_idx - 1 > -1:
                prev_task = tasks[task_idx - 1]
                await self.cancel_task(user=user, task=task)
                await self.execute_task(user=user, task=prev_task)
        except IndexError:
            pass

    async def on_button_pressed(self, keyboard: Keyboard, button: str, user: TelegramUser, **kwargs):
        if isinstance(keyboard, ReplyKeyboard):
            if 'back' in button:
                await self.prev_task(user=user)
            elif 'cancel' in button:
                await self.back(user=user)
