from enum import Enum


class State:
    class Status(Enum):
        DONE = 0

    def __init__(self):
        self._status = self.Status.DONE

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, status: Status):
        if isinstance(status, self.Status):
            self._status = status

    def reset(self):
        self._status = self.Status.DONE
