import aiogram

from tbf.view import View
from aiogram import types
from .models import *


class MainView(View):
    class Meta:
        default = True
        path = 'main'

    async def handle_command(self, command: types.Message, *args, user: TelegramUser, **kwargs):
        print(user)
