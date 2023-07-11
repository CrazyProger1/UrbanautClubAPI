from tbf.page import Page
from .tasks import *
from .creation_state import ObjectCreationState


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
        elif 'about' in button:
            await self.next(user=user, page=AboutPage)


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
        # elif 'by_name' in button:
        #     await self.next(user=user, page=SearchByNamePage)


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


class SearchByNamePage(BasePage):
    object_classes = (

    )
    task_classes = (

    )

    class Meta:
        default = False
        path = 'main.search.by_name'

    async def on_initialize(self, user: TelegramUser):
        pass
        # await self.execute_task(user=user, task=SendAllObjectsTask)


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
        task: Task = self.get_last_executed_task(user=user)

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


class AboutPage(BasePage):
    object_classes = (
        AboutKeyboard,
    )

    class Meta:
        default = False
        path = 'main.about'
