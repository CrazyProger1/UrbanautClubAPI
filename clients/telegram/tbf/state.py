from dataclasses import dataclass
from database.model import Model

__states = {}


@dataclass
class UserState:
    user: Model
    current_page = None


def get_state(user) -> UserState:
    try:
        return __states[user.id]
    except KeyError:
        __states[user.id] = UserState(user)
        return __states[user.id]
