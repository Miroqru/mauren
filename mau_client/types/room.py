from datetime import datetime

from pydantic import BaseModel

from mau_client.enums import RoomState
from mau_client.types.game import Game
from mau_client.types.user import User


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
