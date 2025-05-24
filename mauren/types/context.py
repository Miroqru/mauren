"""Игровой контекст."""

from .base import MauObject
from .game import CurrentPlayer, Game


class GameContext(MauObject):
    """Игровой контекст."""

    game: Game
    player: CurrentPlayer
