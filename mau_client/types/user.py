from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    """Пользователь уно."""

    # Основная информация
    id: str
    username: str
    name: str
    avatar_url: str
    gems: int
    create_date: datetime

    # Статистика пользователя для таблицы лидеров
    play_count: int
    win_count: int
    cards_count: int

    # TODO: Может лучше отдельно их подгружать
    # rooms = fields.ReverseRelation["Room"]
    # my_rooms = fields.ReverseRelation["Room"]

    # my_games = fields.ReverseRelation["Game"]
    # win_games = fields.ReverseRelation["Game"]
    # lose_games = fields.ReverseRelation["Game"]
