import inspect
from enum import Enum
from typing import Callable


class EventChannel:
    class Event(Enum):
        pass

    def __init__(self):
        self._subscribers = {}
        self._tasks = []
        self._task_pointer = 0

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

    def wait(self, event: Event, callback: Callable):
        if not callable(callback):
            raise ValueError('callback must be callable')

        if event not in self._subscribers.keys():
            self._subscribers[event] = [callback]
        else:
            self._subscribers[event].insert(0, callback)

    def add_async_task(self, event: Event, callback: Callable):
        self._tasks.append((event, callback))

    def publish(self, event: Event, *args, **kwargs):
        args = list(args)

        if event in self._subscribers.keys():
            for callback in self._subscribers[event]:

                if callback.__self__ != self:
                    args.append(self)

                callback(*args, **kwargs)

    async def async_publish(self, event: Event, *args, **kwargs):
        args = list(args)
        try:
            current_event, current_task = self._tasks[self._task_pointer]

            if event == current_event:
                args_copy = args.copy()
                if inspect.ismethod(current_task) and current_task.__self__ != self:
                    args_copy.insert(0, self)
                self._next_task()
                await current_task(*args, **kwargs)

        except IndexError:
            pass

        if event in self._subscribers.keys():
            for callback in self._subscribers[event]:
                args_copy = args.copy()

                if inspect.ismethod(callback) and callback.__self__ != self:
                    args_copy.insert(0, self)

                res = await callback(*args_copy, **kwargs)
                if res == 'break':
                    return

    def _next_task(self):
        if len(self._tasks) >= self._task_pointer + 1:
            self._task_pointer += 1

    def switch_task(self, shift: int = 1):
        self._task_pointer += shift

        if len(self._tasks) <= self._task_pointer:
            self._task_pointer = len(self._tasks) - 1
        elif self._task_pointer < 0:
            self._task_pointer = 0

    @property
    def task_pointer(self) -> int:
        return self._task_pointer

    def clear_tasks(self):
        self._task_pointer = 0
        self._tasks.clear()
