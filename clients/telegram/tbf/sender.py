import aiogram

from aiogram import types
from .models import TelegramUser
from conf import settings
from utils import cls_utils
from .translator import _


class Sender(metaclass=cls_utils.SingletonMeta):
    def __init__(self, bot: aiogram.Bot = None):
        self._aiogram_bot = bot

    @property
    def bot(self) -> aiogram.Bot:
        return self._aiogram_bot

    async def send_message(self, user: TelegramUser, text: str, **kwargs) -> types.Message:
        return await self._aiogram_bot.send_message(
            user.id,
            text,
            **kwargs,
            parse_mode=settings.MESSAGES.PARSE_MODE
        )

    async def send_location(self, user: TelegramUser, latitude, longitude, **kwargs):
        return await self._aiogram_bot.send_location(
            chat_id=user.id,
            latitude=latitude,
            longitude=longitude,
            **kwargs
        )

    async def send_translated(self, user: TelegramUser, key: str, **kwargs) -> types.Message:
        format_kwargs = kwargs.pop('format_kwargs', {})
        return await self.send_message(user, _(key, user=user).format(**format_kwargs), **kwargs)

    async def send_long_message(self, user: TelegramUser, text: str, **kwargs):
        pass

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
