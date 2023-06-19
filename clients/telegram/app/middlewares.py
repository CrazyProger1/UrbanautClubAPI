from aiogram import types
from tbf.middleware import Middleware
from conf import settings
from .models import TelegramUser


class AuthMiddleware(Middleware):
    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        tg_user = message_or_callback.from_user
        db_user = TelegramUser.get_or_none(id=tg_user.id)

        if not db_user:
            db_user = TelegramUser.create(
                id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
            )

        return await method(message_or_callback, user=db_user, **kwargs)
