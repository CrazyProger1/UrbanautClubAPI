from tbf.keyboards import ReplyKeyboard


class MainKeyboard(ReplyKeyboard):
    button_keys = (
        'keyboards.main.buttons.search_objects',
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
