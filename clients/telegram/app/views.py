import aiogram

from tbf.view import View
from aiogram import types
from .models import *


class MainView(View):
    class Meta:
        default = True
        path = 'main'

    async def initialize(self, user: TelegramUser):
        pass

    async def handle_command(self, command: types.Message, user: TelegramUser, **kwargs):
        print(command, user, kwargs)
