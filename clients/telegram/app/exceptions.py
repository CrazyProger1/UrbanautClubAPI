class ValidationError(Exception):
    def __init__(self, message_key: str, **format_kwargs):
        self.message_key = message_key
        self.format_kwargs = format_kwargs
