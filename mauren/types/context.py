"""Игровой контекст."""

from pydantic import BaseModel

from mauren.types.game import CurrentPlayer, Game


class GameContext(BaseModel):
    """Игровой контекст."""

    game: Game
    player: CurrentPlayer
