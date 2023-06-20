import functools

import aiogram
from aiogram import types
from enum import Enum
from utils import cls_utils, events
from .models import Language, TelegramUser
from .ui import UIObject
from .translator import _


class Keyboard(UIObject):
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
    def get_button_keys(self) -> tuple[str]:
        return self.button_keys

    @functools.cache
    def get_buttons(self, language: Language):
        pass

    @functools.cache
    def get_markup(self, language: Language):
        raise NotImplementedError

    @functools.cache
    def get_caption(self, language: Language):
        try:
            return _(self.Meta.caption_key, language=language)
        except AttributeError:
            raise AttributeError('Meta.caption_key not specified')


class ReplyKeyboard(Keyboard):

    def __init__(self, *args, **kwargs):
        super(ReplyKeyboard, self).__init__(*args, **kwargs)

        self.subscribe(self.Event.ATTACH, self._on_attach)

    def _on_attach(self, *args, **kwargs):
        if self.parent_view:
            self.parent_view.subscribe(self.parent_view.Event.MESSAGE, self._check_pressed)

    @functools.cache
    def get_translation_key_pairs(self, language: Language):
        result = {}
        for key in self.get_button_keys():
            translation = _(key, language=language)
            result.update({translation: key})
        return result

    @functools.cache
    def get_buttons(self, language: Language):
        result, row = [], []
        for button_key in self.get_button_keys():
            if len(row) == self.row_width:
                result.append(row)
                row = []

            translated = _(button_key, language=language)
            row.append(types.KeyboardButton(translated))

        if len(row) > 0:
            result.append(row)
        return result

    @functools.cache
    def get_markup(self, language: Language):
        return types.ReplyKeyboardMarkup(
            self.get_buttons(language=language),
            row_width=self.row_width
        )

    async def show(self, user: TelegramUser):
        markup = self.get_markup(language=user.language)

        msg = await self._sender.send_message(
            user,
            self.get_caption(language=user.language),
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

    async def _check_pressed(self, view, message: types.Message, user: TelegramUser, *args, **kwargs):
        if self.visible:
            text = message.text
            button = self.get_translation_key_pairs(language=user.language).get(text)

            if button:
                await self.async_publish(
                    self.Event.BUTTON_PRESSED,
                    button=button,
                    user=user,
                    message=message
                )
