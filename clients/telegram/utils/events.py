from enum import Enum
from typing import Callable


class EventChannel:
    class Event(Enum):
        pass

    def __init__(self):
        self._subscribers = {}

    def unsubscribe(self, event: Event, callback: Callable):
        if event and event in self._subscribers.keys():
            self._subscribers[event] = list(
                filter(
                    lambda x: x is not callback,
                    self._subscribers[event]
                )
            )

    def subscribe(self, event: Event, callback: Callable):
        if not callable(callback):
            raise ValueError('callback must be callable')

        if event not in self._subscribers.keys():
            self._subscribers[event] = [callback]
        else:
            self._subscribers[event].append(callback)

    def publish(self, event: Event, *args, **kwargs):
        args = list(args)

        if event in self._subscribers.keys():
            for callback in self._subscribers[event]:

                if callback.__self__ != self:
                    args.append(self)

                callback(*args, **kwargs)

    async def async_publish(self, event: Event, *args, **kwargs):
        args = list(args)

        if event in self._subscribers.keys():
            for callback in self._subscribers[event]:

                if callback.__self__ != self:
                    args.append(self)

                await callback(*args, **kwargs)
