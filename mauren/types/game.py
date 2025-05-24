from datetime import datetime

from mauren.enums import CardBehavior, CardColor

from .base import MauObject


class Card(MauObject):
    """Игровая карта."""

    color: CardColor
    behavior: CardBehavior
    value: int
    cost: int


class Player(MauObject):
    """Игрок в комнате."""

    user_id: str
    name: str
    hand: int | list[Card]
    shotgun_current: int


class OtherPlayer(Player):
    """Прочие игроки."""

    hand: int


class CurrentPlayer(Player):
    """Текущий игрок."""

    hand: list[Card]


class Game(MauObject):
    """Сохранённая игровая сессия.

    Игровые сессии можно будет посмотреть в истории игр комнаты.
    А также в профиле пользователя.
    """

    id: str
    create_time: datetime
    end_time: datetime
    owner: OtherPlayer
    winners: list[OtherPlayer]
    losers: list[OtherPlayer]
