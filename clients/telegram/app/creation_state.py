class ObjectCreationState:
    def __init__(self):
        self._data: dict = {}
        self._step = 0

    def reset(self):
        self._data = {}
        self._step = 0

    def next_step(self):
        self._step += 1

    def prev_step(self):
        if self._step > 0:
            self._step -= 1

    @property
    def step(self):
        return self._step

    @property
    def data(self):
        return self._data
