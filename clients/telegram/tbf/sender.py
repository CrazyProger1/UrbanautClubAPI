import aiogram

from aiogram import types
from .models import TelegramUser
from conf import settings
from utils import cls_utils
from .translator import _


class Sender(metaclass=cls_utils.SingletonMeta):
    def __init__(self, bot: aiogram.Bot = None):
        self._aiogram_bot = bot

    async def send_message(self, user: TelegramUser, text: str = '', **kwargs) -> types.Message:
        return await self._aiogram_bot.send_message(
            user.id,
            text,
            **kwargs,
            parse_mode=settings.MESSAGES.PARSE_MODE
        )

    async def send_message_to_all(self, key: str, **kwargs) -> list[types.Message]:
        result = []
        for user in TelegramUser.select():
            result.append(await self.send_message(user, _(key, user=user), **kwargs))

        return result

    async def send_photo(self, user: TelegramUser, path: str, **kwargs) -> types.Message:
        with open(path, 'rb') as f:
            return await self._aiogram_bot.send_photo(
                user.id,
                f,
                **kwargs
            )
