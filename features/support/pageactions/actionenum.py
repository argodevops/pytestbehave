"""pythons Enum"""

from enum import Enum, auto, unique


@unique
class Action(Enum):
    COPY = auto()
    PASTE = auto()
    RIGHT_CLICK = auto()
    ENTER_KEY = auto()
    TAB_ON = auto()
    DELETE_TEXT = auto()
    CLICK = auto()
    JAVASCRIPT_CLICK = auto()
    DOUBLE_CLICK = auto()
