import aiogram

from tbf.view import View
from aiogram import types
from .models import *


class MainView(View):
    class Meta:
        default = True
        path = 'main'
