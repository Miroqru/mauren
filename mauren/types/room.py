from datetime import datetime

from mauren.enums import RoomState

from .base import MauObject
from .game import Game
from .user import User


class Room(MauObject):
    """Игровая комната."""

    # Информация о комнате
    id: str
    name: str
    create_time: datetime
    private: bool

    # Участники
    owner: User
    players: list[User]

    # Настройки комнаты
    gems: int
    max_players: int
    min_players: int

    # Статус комнаты
    status: RoomState
    status_updates: datetime

    # История игр комнаты
    games: list[Game]


class RoomEdit(MauObject):
    """Данные о комнате, которые можно изменить."""

    name: str | None = None
    private: bool | None = None
    room_password: str | None = None
    gems: int | None = None
    max_players: int | None = None
    min_players: int | None = None


class RoomDelete(MauObject):
    """Данные комнаты при удалении."""

    room_id: str
