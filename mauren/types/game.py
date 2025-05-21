from datetime import datetime

from mauren.types.user import User
from pydantic import BaseModel


class Game(BaseModel):
    """Сохранённая игровая сессия.

    Игровые сессии можно будет посмотреть в истории игр комнаты.
    А также в профиле пользователя.
    """

    id: str
    create_time: datetime
    end_time: datetime
    owner: User
    winners: list[User]
    losers: list[User]
