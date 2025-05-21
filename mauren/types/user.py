from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    """Пользователь уно."""

    # Основная информация
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


class UserEdit(BaseModel):
    """Данные о пользователе для изменения."""

    username: str | None = None
    name: str | None = None
    avatar_url: str | None = None


class UserCredentials(BaseModel):
    """Данные пользователя для регистрации и входа."""

    username: str
    password: str


class UserChangePassword(BaseModel):
    """Данные пользователя для смены пароля."""

    old_password: str
    new_password: str


class TokenResult(BaseModel):
    """Результат при получении токена."""

    status: str
    token: str
