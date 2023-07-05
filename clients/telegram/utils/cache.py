import functools
import gc
from typing import Callable


def clear_cache(fltr: Callable[[functools._lru_cache_wrapper], bool] = None):
    gc.collect()
    wrappers = [
        a for a in gc.get_objects()
        if isinstance(a, functools._lru_cache_wrapper)
    ]

    for wrapper in wrappers:
        if callable(fltr):
            fltr(wrapper)
        wrapper.cache_clear()
