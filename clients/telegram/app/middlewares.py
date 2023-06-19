from aiogram import types
from tbf.middleware import Middleware


class AuthMiddleware(Middleware):
    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        return await method(message_or_callback, user=None, **kwargs)


