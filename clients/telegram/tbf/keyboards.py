import functools

import aiogram
from aiogram import types
from enum import Enum
from utils import cls_utils, events
from .models import Language, TelegramUser
from .ui import UIObject
from .translator import _


class KeyboardMeta(cls_utils.MetaChecker, cls_utils.SingletonMeta):
    _default_values = {
        'autoshow': False,
        'autohide': False
    }
    _required_meta_fields = (
        'caption_key',
    )


class Keyboard(UIObject, metaclass=KeyboardMeta):
    button_keys: tuple[str] = (

    )
    row_width: int = 1

    class Meta:
        caption_key: str = ''
        autoshow: bool = False
        autohide: bool = False

    class Event(Enum):
        INITIALIZE = 1
        DESTROY = 2
        SHOW = 3
        HIDE = 4
        ATTACH = 5
        DETACH = 6
        BUTTON_PRESSED = 7

    @functools.cache
    def get_translation_key_pairs(self, language: Language):
        result = {}
        for key in self.get_button_keys():
            translation = _(key, language=language)
            result.update({translation: key})
        return result

    @functools.cache
    def get_button_keys(self) -> tuple[str] | list[str]:
        return self.button_keys

    @functools.cache
    def get_buttons(self, user: TelegramUser):
        pass

    @functools.cache
    def get_markup(self, user: TelegramUser):
        raise NotImplementedError

    @functools.cache
    def get_caption(self, user: TelegramUser):
        try:
            return _(self.Meta.caption_key, user)
        except AttributeError:
            raise AttributeError('Meta.caption_key not specified')


class ReplyKeyboard(Keyboard):

    def __init__(self, *args, **kwargs):
        super(ReplyKeyboard, self).__init__(*args, **kwargs)

        self.subscribe(self.Event.ATTACH, self._on_attach)

    def _on_attach(self, *args, **kwargs):
        if self.parent_page:
            self.parent_page.subscribe(self.parent_page.Event.MESSAGE, self._check_pressed)

    async def _check_pressed(self, view, message: types.Message, user: TelegramUser, *args, **kwargs):
        if self.is_visible(user=user):
            text = message.text
            button = self.get_translation_key_pairs(language=user.language).get(text)

            if button:
                await self.async_publish(
                    self.Event.BUTTON_PRESSED,
                    button=button,
                    user=user,
                    message=message
                )
                return 'break'

    @functools.cache
    def get_buttons(self, user: TelegramUser):
        result, row = [], []
        for button_key in self.get_button_keys():
            if len(row) == self.row_width:
                result.append(row)
                row = []

            translated = _(button_key, user)
            row.append(types.KeyboardButton(translated))

        if len(row) > 0:
            result.append(row)
        return result

    @functools.cache
    def get_markup(self, user: TelegramUser):
        return types.ReplyKeyboardMarkup(
            self.get_buttons(user),
            row_width=self.row_width
        )

    async def show(self, user: TelegramUser):
        markup = self.get_markup(user)

        msg = await self.sender.send_message(
            user,
            self.get_caption(user),
            reply_markup=markup
        )
        user.state.reply_keyboard_message_id = msg.message_id

        await super(ReplyKeyboard, self).show(user)

    async def hide(self, user: TelegramUser):
        try:
            msgid = user.state.reply_keyboard_message_id
        except AttributeError:
            return

        if msgid:
            try:
                await self._aiogram_bot.delete_message(user.id, msgid)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass

            await super(ReplyKeyboard, self).hide(user)


class InlineKeyboard(Keyboard):
    callback_data_length = 20

    def __init__(self, *args, **kwargs):
        super(InlineKeyboard, self).__init__(*args, **kwargs)

        self.subscribe(self.Event.ATTACH, self._on_attach)

    def _on_attach(self, *args, **kwargs):
        if self.parent_page:
            self.parent_page.subscribe(self.parent_page.Event.CALLBACK, self._check_pressed)

    @functools.cache
    def get_buttons(self, user: TelegramUser) -> list[list[types.KeyboardButton | types.InlineKeyboardButton]]:
        result, row = [], []
        for i, button_key in enumerate(self.get_button_keys()):
            if len(row) == self.row_width:
                result.append(row)
                row = []

            translated = _(button_key, user)
            row.append(types.InlineKeyboardButton(translated, callback_data=f'{id(self)}:{i}'))

        if len(row) > 0:
            result.append(row)
        return result

    @functools.cache
    def get_markup(self, user: TelegramUser) -> types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(
            row_width=self.row_width
        )
        for btn_row in self.get_buttons(user):
            markup.add(*btn_row)
        return markup

    async def show(self, user: TelegramUser):
        markup = self.get_markup(user)
        await super(InlineKeyboard, self).show(user)
        msg = await self.sender.send_message(
            user,
            self.get_caption(user),
            reply_markup=markup
        )
        user.state.inline_keyboard_message_id = msg.message_id

    async def hide(self, user: TelegramUser):
        try:
            msgid = user.state.inline_keyboard_message_id
        except AttributeError:
            return

        if msgid:
            try:
                await self._aiogram_bot.delete_message(user.id, msgid)
            except aiogram.utils.exceptions.MessageToDeleteNotFound:
                pass
            await super(InlineKeyboard, self).hide(user)

    @functools.cache
    def get_pressed(self, text: str, language: Language) -> str | None:
        keyboard_id, button_index = text.split(':')
        if int(keyboard_id) == id(self):
            return self.get_button_keys()[int(button_index)]

    async def _check_pressed(self, view, callback: types.CallbackQuery, user: TelegramUser, *args, **kwargs):
        button = self.get_pressed(callback.data, user.language)
        if button:
            await self.async_publish(
                self.Event.BUTTON_PRESSED,
                button=button,
                user=user,
                callback=callback
            )
            return 'break'
