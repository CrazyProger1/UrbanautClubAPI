import aiogram

from aiogram import types
from utils import cls_utils, cache
from .page import Page
from .state import UserState
from .enums import ContentType
from .middlewares import Middleware
from .models import TelegramUser


class Router(metaclass=cls_utils.SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self._aiogram_bot = bot
        self._user_states = {}
        self._middleware_list = None

        self._initialize_middlewares()
        self._initialize_pages()

    @property
    def bot(self) -> aiogram.Bot:
        return self._aiogram_bot

    def _initialize_middlewares(self):
        self._middleware_list = list(map(lambda m: m(self._aiogram_bot), cls_utils.iter_subclasses(Middleware)))

    def _initialize_pages(self):
        for page in cls_utils.iter_subclasses(Page):
            page(self._aiogram_bot, self.set_page)

    @staticmethod
    def _middlewares(content_type: ContentType):
        def decorator(method):
            async def wrapper(self, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
                index = 0

                async def next_step(*args, **kwgs):
                    nonlocal index
                    try:
                        middleware = self._middleware_list[index]
                    except IndexError:
                        return await method(self, *args, **kwgs)

                    index += 1
                    return await middleware(next_step, *args, **kwgs)

                return await next_step(message_or_callback, **kwargs, content_type=content_type)

            return wrapper

        return decorator

    async def get_current_page(self, user: TelegramUser) -> Page:
        if not user.state.current_page:
            default_page = Page.get_default()
            assert default_page is not None, 'Default page not set'
            await self.set_page(user, default_page)
        return user.state.current_page

    async def reset_page(self, user: TelegramUser):
        await self.set_page(user, user.state.current_page)

    async def set_page(self, user: TelegramUser, page: str | Page | type[Page]):
        if isinstance(page, str):
            page_obj = Page.get(page)
            if not page_obj:
                raise ValueError(f'Page with that path does not exists: {page}')
            page = page_obj

        if not isinstance(page, Page):
            if issubclass(page, Page):
                page = page()
            else:
                raise ValueError('page must be a type of Page or instance of Page or Page path')

        if user.state.current_page:
            await user.state.current_page.async_publish(page.Event.DESTROY, user)

        await page.async_publish(page.Event.INITIALIZE, user)

        user.state.current_page = page

    async def check_language_changed(self, user: TelegramUser):
        if user.state.language_changed:
            def has_user_param(wrapper):
                try:
                    annotations = wrapper.__annotations__
                    return 'user' not in annotations.keys()
                except AttributeError:
                    pass
                return True

            cache.clear_cache(fltr=has_user_param)
            await self.reset_page(user=user)

    @_middlewares(content_type=ContentType.CALLBACK)
    async def route_callback(self, *args, **kwargs):
        user = kwargs.get('user')
        await self.check_language_changed(user=user)
        page = await self.get_current_page(user=user)
        await page.async_publish(page.Event.CALLBACK, *args, **kwargs)

    @_middlewares(content_type=ContentType.MESSAGE)
    async def route_message(self, *args, **kwargs):
        user = kwargs.get('user')
        await self.check_language_changed(user=user)
        page = await self.get_current_page(user=user)
        await page.async_publish(page.Event.MESSAGE, *args, **kwargs)

    @_middlewares(content_type=ContentType.COMMAND)
    async def route_command(self, *args, **kwargs):
        user = kwargs.get('user')
        await self.check_language_changed(user=user)
        page = await self.get_current_page(user=user)
        await page.async_publish(page.Event.COMMAND, *args, **kwargs)

    @_middlewares(content_type=ContentType.MEDIA)
    async def route_media(self, *args, **kwargs):
        user = kwargs.get('user')
        await self.check_language_changed(user=user)
        page = await self.get_current_page(user=user)
        await page.async_publish(page.Event.MEDIA, *args, **kwargs)
