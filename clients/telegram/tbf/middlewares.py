import aiogram

from utils import cls_utils
from aiogram import types
from .models import *


class Middleware(metaclass=cls_utils.SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self._aiogram_bot = bot

    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        return await method(message_or_callback, **kwargs)


class AuthMiddleware(Middleware):
    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        tg_user = message_or_callback.from_user
        db_user = TelegramUser.get_or_none(id=tg_user.id)
        language = Language.get_or_none(short_name=tg_user.locale.language) or Language.get_default()

        if not db_user:
            db_user = TelegramUser.create(
                id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                language=language
            )

        return await method(message_or_callback, user=db_user, **kwargs)
