import functools

from tbf.keyboards import ReplyKeyboard, InlineKeyboard, Keyboard
from tbf.models import TelegramUser
from tbf.translator import _

from .models import AbandonedObjectCategory, Country
from .address import get_address


class MainKeyboard(ReplyKeyboard):
    button_keys = (
        'keyboards.main.buttons.search_objects',
        'keyboards.main.buttons.add_object'
    )

    class Meta:
        caption_key = 'keyboards.main.caption'
        autoshow = True
        autohide = True


class SearchObjectsKeyboard(ReplyKeyboard):
    button_keys = (
        'keyboards.search.buttons.all',
        'keyboards.common.back',
    )

    class Meta:
        caption_key = 'keyboards.search.caption'
        autoshow = True
        autohide = True


class AllObjectsNavKeyboard(ReplyKeyboard):
    row_width = 2
    button_keys = (
        'keyboards.common.prev',
        'keyboards.common.next',
        'keyboards.common.back',
    )

    class Meta:
        caption_key = 'keyboards.search.all.caption'
        autoshow = True
        autohide = True


class AddObjectKeyboard(ReplyKeyboard):
    row_width = 2
    button_keys = (
        'keyboards.common.back',
        'keyboards.common.cancel',
    )

    class Meta:
        caption_key = 'keyboards.add_object.caption'
        autoshow = True
        autohide = True


class CreateObjectConfirmationKeyboard(InlineKeyboard):
    row_width = 2
    button_keys = (
        'keyboards.common.create',
        'keyboards.common.cancel',
    )

    class Meta:
        caption_key = 'keyboards.add_object.confirmation.caption'
        autoshow = False
        autohide = True

    def get_caption(self, user: TelegramUser):
        state = user.state.ocs

        data = state.data

        return _(
            'contents.objects.object_form',
            user
        ).format(
            name=data['name'],
            desc=data['description'],
            category=_(f'contents.objects.categories.{data["category"]}', user, default=data['category']),
            state=_(f'contents.objects.states.{data["state"]}', user),
            address=get_address(data['street_number'], data['street'], data['city'], data['country']),
            latitude=data['latitude'],
            longitude=data['longitude']
        )


class SelectObjectCategoryKeyboard(InlineKeyboard):
    row_width = 3
    button_keys = (

    )

    class Meta:
        caption_key = 'keyboards.add_object.select_category.caption'
        autoshow = False
        autohide = True

    @functools.cache
    def get_button_keys(self) -> tuple[str] | list[str]:
        categories = []
        for category in AbandonedObjectCategory.select():
            categories.append(
                f'contents.objects.categories.{category.name}'
            )

        return categories


class SelectObjectStateKeyboard(InlineKeyboard):
    row_width = 1
    button_keys = (
        'contents.objects.states.d',
        'contents.objects.states.b',
        'contents.objects.states.a',
        'contents.objects.states.g',
        'contents.objects.states.n'
    )

    class Meta:
        caption_key = 'keyboards.add_object.select_state.caption'
        autoshow = False
        autohide = True
