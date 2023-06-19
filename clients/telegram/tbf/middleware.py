import aiogram

from utils import cls_utils
from aiogram import types


class Middleware(metaclass=cls_utils.SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self._aiogram_bot = bot

    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        return await method(message_or_callback, **kwargs)
