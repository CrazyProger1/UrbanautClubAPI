import functools
import aiogram

from aiogram import types
from typing import Optional
from utils import cls_utils
from database.models import TelegramUser


class Page:
    default: bool = False
    path: str = ''

    @classmethod
    @functools.cache
    def get(cls, path: str) -> Optional[type["Page"]]:
        for page in cls_utils.iter_subclasses(cls):
            if page.path == path:
                return page

    @classmethod
    @functools.cache
    def get_default(cls) -> Optional[type["Page"]]:
        for page in cls_utils.iter_subclasses(cls):
            if page.default:
                return page

    async def initialize(self, user: TelegramUser):
        pass

    async def destroy(self, user: TelegramUser):
        pass

    async def handle_message(self, message: types.Message, user: TelegramUser, **kwargs):
        pass

    async def handle_callback(self, callback: types.CallbackQuery, user: TelegramUser, **kwargs):
        pass

    async def handle_media(self, message: types.Message, user: TelegramUser, **kwargs):
        pass

    async def handle_command(self, message: types.Message, user: TelegramUser, **kwargs):
        pass
