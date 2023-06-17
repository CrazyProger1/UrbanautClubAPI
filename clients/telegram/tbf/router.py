import aiogram

from utils.cls_utils import SingletonMeta


class Router(metaclass=SingletonMeta):
    def __init__(self, aiogram_bot: aiogram.Bot):
        self._aiogram_bot = aiogram_bot

    async def route_callback(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.handle_callback(*args, **kwargs)

    async def route_message(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.handle_message(*args, **kwargs)

    async def route_command(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.handle_command(*args, **kwargs)

    async def route_media(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.handle_media(*args, **kwargs)
