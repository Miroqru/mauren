from datetime import datetime

from pydantic import BaseModel

from mauren.enums import RoomState
from mauren.types.game import Game
from mauren.types.user import User


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


class RoomEdit(BaseModel):
    """Данные о комнате, которые можно изменить."""

    name: str | None = None
    private: bool | None = None
    room_password: str | None = None
    gems: int | None = None
    max_players: int | None = None
    min_players: int | None = None


class RoomDelete(BaseModel):
    """Данные комнаты при удалении."""

    room_id: str
