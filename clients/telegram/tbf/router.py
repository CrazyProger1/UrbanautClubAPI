import aiogram

from aiogram import types
from utils import cls_utils
from .view import View
from .state import UserState
from .enums import ContentType
from .middleware import Middleware


class Router(metaclass=cls_utils.SingletonMeta):
    def __init__(self, aiogram_bot: aiogram.Bot):
        self._aiogram_bot = aiogram_bot
        self._user_states = {}
        self._middleware_list = list(map(lambda m: m(self._aiogram_bot), cls_utils.iter_subclasses(Middleware)))

    @staticmethod
    def _middlewares(content_type: ContentType):
        def decorator(method):
            async def wrapper(self, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
                index = 0

                async def next_step(*args, **kwgs):
                    nonlocal index
                    try:
                        middleware = self._middleware_list[index]
                    except IndexError:
                        return await method(self, *args, **kwgs)

                    index += 1
                    return await middleware(next_step, *args, **kwgs)

                return await next_step(message_or_callback, **kwargs, content_type=content_type)

            return wrapper

        return decorator

    async def get_current_view(self, user) -> View:
        state = await self.get_current_state(user)
        return state.current_view

    async def get_current_state(self, user) -> UserState:
        try:
            return self._user_states[user]
        except KeyError:
            self._user_states[user] = UserState(user, None)
            await self.set_view(user, View.get_default())
            return self._user_states[user]

    async def set_view(self, user, view: str | View):
        if isinstance(view, str):
            view_obj = View.get(view)
            if not view_obj:
                raise ValueError(f'View with that path does not exists: {view}')
            view = view_obj

        state = await self.get_current_state(user)

        if state.current_view:
            await state.current_view.destroy(user)

        await view.initialize(user)
        state.current_view = view

    @_middlewares(content_type=ContentType.CALLBACK)
    async def route_callback(self, *args, **kwargs):
        view = await self.get_current_view(kwargs.get('user'))
        await view.handle_callback(*args, **kwargs)

    @_middlewares(content_type=ContentType.MESSAGE)
    async def route_message(self, *args, **kwargs):
        view = await self.get_current_view(kwargs.get('user'))
        await view.handle_message(*args, **kwargs)

    @_middlewares(content_type=ContentType.COMMAND)
    async def route_command(self, *args, **kwargs):
        view = await self.get_current_view(kwargs.get('user'))
        await view.handle_command(*args, **kwargs)

    @_middlewares(content_type=ContentType.MEDIA)
    async def route_media(self, *args, **kwargs):
        view = await self.get_current_view(kwargs.get('user'))
        await view.handle_media(*args, **kwargs)
