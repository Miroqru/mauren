"""Главный класс для взаимодействия с сервером."""

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from loguru import logger

from mauren.enums import LeaderBoardGroups
from mauren.exceptions import MauException, MauRequestError
from mauren.types.room import Room, RoomDelete, RoomEdit
from mauren.types.user import (
    TokenResult,
    User,
    UserChangePassword,
    UserCredentials,
    UserEdit,
)

_DEFAULT_SERVER = "https://mau.miroq.ru/api/"


class Mau:
    """Взаимодействие с сервером."""

    def __init__(self, server: str = _DEFAULT_SERVER) -> None:
        self.server = server
        self.session = ClientSession(self.server)

    async def close(self) -> None:
        await self.session.close()

    async def _request(self, url: str, method: str = "get", **options):
        try:
            async with self.session.request(method, url, **options) as r:
                logger.debug("{} {}", url, r.status)

                if r.status == 200:
                    return await r.json()
                raise MauRequestError(r.status, await r.text())
        except ContentTypeError as e:
            raise MauException(f"Failed to parse: {e}") from e

    # Get rooms
    # =========

    async def rooms(self) -> list[Room]:
        """Возвращает список всех открытых комнат."""
        res = await self._request("/rooms")
        return [Room.validate(r) for r in res]

    async def random_room(self) -> Room:
        """Возвращает случайную открытую комнату."""
        res = await self._request("/rooms/random")
        return Room.validate(res)

    async def room(self, room_id: str) -> Room:
        """Возвращает список всех открытых комнат."""
        res = await self._request(f"/rooms/{room_id}")
        return Room.validate(res)

    # Control rooms
    # =============

    async def active_room(self, token: str) -> Room:
        """Возвращает список всех открытых комнат."""
        res = await self._request(
            "/rooms/active", headers=[("Authorization", f"Bearer {token}")]
        )
        return Room.validate(res)

    async def create_room(self, token: str) -> Room:
        """Создаёт новую комнату."""
        res = await self._request(
            "/rooms", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return Room.validate(res)

    async def edit_room(self, token: str, room: RoomEdit) -> Room:
        """Обновляет данные комнаты."""
        res = await self._request(
            "/rooms/",
            method="put",
            headers=[("Authorization", f"Bearer {token}")],
            json=room.model_dump(),
        )
        return Room.validate(res)

    async def delete_room(self, token: str, room_id: str) -> RoomDelete:
        """Удаляет комнату по её ID."""
        res = await self._request(
            f"/rooms/{room_id}",
            method="delete",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return RoomDelete.validate(res)

    async def join_room(self, token: str, room_id: str) -> Room:
        """Заходит в комнату."""
        res = await self._request(
            f"/rooms/{room_id}/join",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return Room.validate(res)

    async def leave_room(self, token: str, room_id: str) -> Room:
        """Покидает комнату."""
        res = await self._request(
            f"/rooms/{room_id}/leave",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return Room.validate(res)

    async def room_kick(self, token: str, room_id: str, user_id: str) -> Room:
        """Выгоняет игрока из комнаты."""
        res = await self._request(
            f"/rooms/{room_id}/kick/{user_id}",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return Room.validate(res)

    async def room_owner(self, token: str, room_id: str, user_id: str) -> Room:
        """Изменяет владельца комнаты."""
        res = await self._request(
            f"/rooms/{room_id}/owner/{user_id}",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return Room.validate(res)

    # Leaderboard
    # ===========

    async def rating(
        self, category: LeaderBoardGroups = LeaderBoardGroups.GEMS
    ) -> list[User]:
        """Таблица лидеров по категории."""
        res = await self._request(f"/leaderboard/{category}")
        return [User.validate(u) for u in res]

    async def player_rating(
        self, username: str, category: LeaderBoardGroups = LeaderBoardGroups.GEMS
    ) -> int:
        """Положение пользователя в таблице лидеров по категории."""
        res = await self._request(f"/leaderboard/{username}/{category}")
        return res

    # Users
    # =====

    async def users(self) -> list[User]:
        """Возвращает список пользователей."""
        res = await self._request("/users")
        return [User.validate(u) for u in res]

    async def user(self, username: str) -> User:
        """Получает пользователя по username."""
        res = await self._request(f"/users/{username}")
        return User.validate(res)

    async def register_user(self, user: UserCredentials) -> User:
        """Регистрирует нового пользователя."""
        res = await self._request("/users", method="post", json=user.model_dump())
        return User.validate(res)

    # Authorized users
    # ================

    async def user_me(self, token: str) -> User:
        """Возвращает актуальные данные пользователя."""
        res = await self._request(
            "/users/me", headers=[("Authorization", f"Bearer {token}")]
        )
        return User.validate(res)

    async def login_user(self, user: UserCredentials) -> TokenResult:
        """Возвращает токен пользователя."""
        res = await self._request("/users/login", method="post", json=user.model_dump())
        return TokenResult.validate(res)

    async def edit_user(self, token: str, params: UserEdit) -> User:
        """Обновляет данные пользователя."""
        res = await self._request(
            "/users/",
            method="put",
            headers=[("Authorization", f"Bearer {token}")],
            json=params.model_dump(),
        )
        return User.validate(res)

    async def change_password(self, token: str, password: UserChangePassword) -> User:
        """Изменяет пароль для пользователя."""
        res = await self._request(
            "/users/change-password",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
            json=password.model_dump(),
        )
        return User.validate(res)
