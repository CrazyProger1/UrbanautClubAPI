import sys
import aiogram

from aiogram import types
from conf import settings


class App:
    def __init__(self):
        self._bot = aiogram.Bot(token=settings.BOT.TOKEN)
        self._dispatcher = aiogram.Dispatcher(bot=self._bot)

    async def _handle_callback(self, *args, **kwargs):
        await self._router.route_callback(*args, **kwargs)

    async def _handle_message(self, *args, **kwargs):
        await self._router.route_message(*args, **kwargs)

    async def _handle_command(self, *args, **kwargs):
        await self._router.route_command(*args, **kwargs)

    async def _handle_media(self, *args, **kwargs):
        await self._router.route_media(*args, **kwargs)

    def _register_handlers(self):
        self._dispatcher.register_message_handler(
            callback=self._handle_command,
            regexp=settings.COMMAND.REGEXP
        )
        self._dispatcher.register_message_handler(
            callback=self._handle_message
        )
        self._dispatcher.register_message_handler(
            callback=self._handle_media,
            content_types=(
                types.ContentType.AUDIO,
                types.ContentType.VOICE,
                types.ContentType.VIDEO
            )
        )
        self._dispatcher.register_callback_query_handler(
            callback=self._handle_callback
        )

    def run(self):
        self._register_handlers()
        aiogram.executor.start_polling(
            dispatcher=self._dispatcher,
            skip_updates=True
        )
