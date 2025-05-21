from datetime import datetime

from mauren.enums import RoomState
from mauren.types.game import Game
from mauren.types.user import User
from pydantic import BaseModel


class Room(BaseModel):
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
