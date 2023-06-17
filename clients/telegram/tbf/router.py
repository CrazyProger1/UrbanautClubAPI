import aiogram

from utils.cls_utils import SingletonMeta
from .view import View
from .state import UserState


class Router(metaclass=SingletonMeta):
    def __init__(self, aiogram_bot: aiogram.Bot):
        self._aiogram_bot = aiogram_bot
        self._user_states = {}

    async def get_current_view(self, user) -> View:
        state = await self.get_current_state(user)
        return state.current_view

    async def get_current_state(self, user) -> UserState:
        try:
            return self._user_states[user]
        except KeyError:
            self._user_states[user] = UserState(user, View.get_default())
            return self._user_states[user]

    async def route_callback(self, *args, **kwargs):
        view = await self.get_current_view(kwargs.get('user'))
        await view.handle_callback(*args, **kwargs)

    async def route_message(self, *args, **kwargs):
        view = await self.get_current_view(kwargs.get('user'))
        await view.handle_message(*args, **kwargs)

    async def route_command(self, *args, **kwargs):
        view = await self.get_current_view(kwargs.get('user'))
        await view.handle_command(*args, **kwargs)

    async def route_media(self, *args, **kwargs):
        view = await self.get_current_view(kwargs.get('user'))
        await view.handle_media(*args, **kwargs)
