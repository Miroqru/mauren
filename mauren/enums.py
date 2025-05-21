"""Общие перечисления."""

from enum import StrEnum


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
