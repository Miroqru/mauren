"""Пользователь Mau."""

from mauren.api import Mau
from mauren.exceptions import MauException
from mauren.types.user import User, UserChangePassword, UserCredentials, UserEdit


class MauUser:
    """Пользователь Mau.

    Позволяет выполнять запросы от имени конкретного пользователя.
    Автоматически подставляет необходимые данные.
    """

    def __init__(self, client: Mau, username: str) -> None:
        self.client = client
        self.username = username
        self._token: str | None = None

    def _get_token(self) -> str:
        if self._token is None:
            raise MauException("You need to login user before use API")
        return self._token

    # User
    # ====

    async def register(self, password: str) -> User:
        """Регистрирует пользователя с указанными данными."""
        user = await self.client.register_user(
            UserCredentials(username=self.username, password=password)
        )
        await self.login(password)
        return user

    async def me(self) -> User:
        """Возвращает актуальную информацию о пользователе."""
        return await self.client.user_me(self._get_token())

    async def login(self, password: str) -> None:
        """Обновляет токен пользователя."""
        res = await self.client.login_user(
            UserCredentials(username=self.username, password=password)
        )
        self._token = res.token

    async def edit(
        self, name: str | None = None, avatar_url: str | None = None
    ) -> User:
        """Обновляет профиль пользователя."""
        return await self.client.edit_user(
            self._get_token(), UserEdit(name=name, avatar_url=avatar_url)
        )

    async def change_password(self, password: UserChangePassword) -> User:
        """Изменяет пароль пользователя."""
        return await self.client.change_password(self._get_token(), password)
