"""Общие перечисления."""

from enum import IntEnum, StrEnum


class LeaderBoardGroups(StrEnum):
    GEMS = "gems"
    GAMES = "games"
    WINS = "wins"
    CARDS = "cards"


class RoomState(StrEnum):
    """Все возможные состояния игровой комнаты."""

    idle = "idle"
    game = "game"
    ended = "ended"


class CardColor(IntEnum):
    """Доступные цвета карты."""

    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    BLACK = 6
    CREAM = 7


class CardBehavior(StrEnum):
    """Поведение карты."""

    NUMBER = "number"
    TAKE = "take"
    PUt = "put"
    DELTA = "delta"
    TWIST = "twist"
    ROTATE = "rotate"
    TURN = "turn"
    REVERSE = "reverse"
    WILD_COLOR = "wild+color"
    WOLD_TAKE = "wild+take"
