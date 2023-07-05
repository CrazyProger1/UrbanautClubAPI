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
        db_user.username = tg_user.username
        db_user.first_name = tg_user.first_name
        db_user.last_name = tg_user.last_name
        db_user.state.language_changed = db_user.language.short_name != language.short_name
        db_user.language = language
        db_user.save()
        return await method(message_or_callback, user=db_user, **kwargs)
