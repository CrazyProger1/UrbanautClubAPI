from tbf.keyboards import ReplyKeyboard


class MainKeyboard(ReplyKeyboard):
    button_keys = (
        'keyboards.main.buttons.test',
    )

    class Meta:
        caption_key = 'keyboards.main.caption'
        autoshow = True
        autohide = True
