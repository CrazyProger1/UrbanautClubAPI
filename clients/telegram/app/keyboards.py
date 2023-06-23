from tbf.keyboards import ReplyKeyboard, InlineKeyboard


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


class AddObjectConfirmationKeyboard(InlineKeyboard):
    row_width = 2
    button_keys = (
        'keyboards.common.apply',
        'keyboards.common.cancel',
    )

    class Meta:
        caption_key = 'keyboards.add_object.confirmation.caption'
        autoshow = False
        autohide = True
