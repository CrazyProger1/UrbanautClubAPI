class Field:
    def __init__(self):
        pass


class MethodField(Field):
    def __init__(self, getter: str = None, setter: str = None):
        self.getter = getter
        self.setter = setter
        super(MethodField, self).__init__()
