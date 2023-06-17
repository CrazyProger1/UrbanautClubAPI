from dataclasses import dataclass
from database.model import Model
from .view import View


@dataclass
class UserState:
    user: Model
    current_view: View | None
