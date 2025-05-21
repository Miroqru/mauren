"""Главный класс для взаимодействия с сервером."""

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from loguru import logger

from mau_client.enums import LeaderBoardGroups
from mau_client.exceptions import MauException, MauRequestError
from mau_client.types.user import (
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

    # LEADERBOARD
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

    # USERS
    # =====

    async def users(self) -> list[User]:
        """Возвращает список пользователей."""
        res = await self._request("/users")
        return [User.validate(u) for u in res]

    async def user_me(self, token: str) -> User:
        """Возвращает актуальные данные пользователя."""
        res = await self._request(
            "/users/me", headers=[("Authorization", f"Bearer {token}")]
        )
        return User.validate(res)

    async def user(self, username: str) -> User:
        """Получает пользователя по username."""
        res = await self._request(f"/users/{username}")
        return User.validate(res)

    async def register_user(self, user: UserCredentials) -> User:
        """Регистрирует нового пользователя."""
        res = await self._request("/users", method="post", json=user.model_dump())
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
