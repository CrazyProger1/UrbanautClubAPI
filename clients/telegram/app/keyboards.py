from tbf.keyboards import ReplyKeyboard


class MainKeyboard(ReplyKeyboard):
    button_keys = (
        'keyboards.main.buttons.search_objects',
        'keyboards.main.buttons.add_object',
        'keyboards.main.buttons.settings',
    )

    class Meta:
        caption_key = 'keyboards.main.caption'
        autoshow = True
        autohide = True
