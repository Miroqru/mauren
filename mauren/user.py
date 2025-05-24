"""Пользователь Mau."""

from mauren.api import Mau
from mauren.exceptions import MauException
from mauren.types.context import GameContext
from mauren.types.game import CardColor
from mauren.types.room import Room, RoomDelete, RoomEdit
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

    # Game
    # ====

    async def join_game(self) -> GameContext:
        """Добавляет пользователя в игру."""
        return await self.client.join_game(self._get_token())

    async def leave_game(self) -> GameContext:
        """Покинуть игру."""
        return await self.client.leave_game(self._get_token())

    async def active_game(self) -> GameContext:
        """Возвращает актуальный игровой контекст."""
        return await self.client.active_game(self._get_token())

    async def start_game(self) -> GameContext:
        """Начинает игру в комнате."""
        return await self.client.start_game(self._get_token())

    async def end_game(self) -> GameContext:
        """Принудительно завершает игру в комнате."""
        return await self.client.end_game(self._get_token())

    async def game_kick(self, user_id: str) -> GameContext:
        """Выгоняет игрока из игры."""
        return await self.client.game_kick(self._get_token(), user_id)

    async def game_skip(self) -> GameContext:
        """Пропускает текущего игрока в игре."""
        return await self.client.game_skip(self._get_token())

    async def game_next(self) -> GameContext:
        """Передаёт ход следующему игроку."""
        return await self.client.game_next(self._get_token())

    async def game_take(self) -> GameContext:
        """Берёт карты."""
        return await self.client.game_take(self._get_token())

    async def game_shotgun_take(self) -> GameContext:
        """Берёт карты вместо выстрела из револьвера."""
        return await self.client.game_shotgun_take(self._get_token())

    async def game_shotgun_shot(self, taken: str) -> GameContext:
        """Выстреливает из револьвера вместо взятия карт."""
        return await self.client.game_shotgun_shot(self._get_token())

    async def game_bluff(self) -> GameContext:
        """Проверяет прошлого игрока на честность."""
        return await self.client.game_bluff(self._get_token())

    async def game_color(self, color: CardColor) -> GameContext:
        """Выбирает цвет для карты."""
        return await self.client.game_color(self._get_token(), color)

    async def game_player(self, user_id: str) -> GameContext:
        """Выбирает игрока для обмена картами."""
        return await self.client.game_player(self._get_token(), user_id)

    # Room
    # ====

    async def create_room(self) -> Room:
        """Создаёт новую комнату."""
        return await self.client.create_room(self._get_token())

    async def room(self) -> Room:
        """Возвращает активную комнату игрока."""
        return await self.client.active_room(self._get_token())

    async def edit_room(self, room: RoomEdit) -> Room:
        """Изменяет данные комнаты."""
        return await self.client.edit_room(self._get_token(), room)

    async def delete_room(self, room_id: str) -> RoomDelete:
        """Удаляет комнату по её ID."""
        return await self.client.delete_room(self._get_token(), room_id)

    async def join_room(self, room_id: str) -> Room:
        """Удаляет комнату по её ID."""
        return await self.client.join_room(self._get_token(), room_id)

    async def leave_room(self, room_id: str) -> Room:
        """Удаляет комнату по её ID."""
        return await self.client.leave_room(self._get_token(), room_id)

    async def room_kick(self, room_id: str, user_id: str) -> Room:
        """Удаляет комнату по её ID."""
        return await self.client.room_kick(self._get_token(), room_id, user_id)

    async def room_owner(self, room_id: str, user_id: str) -> Room:
        """Удаляет комнату по её ID."""
        return await self.client.room_owner(self._get_token(), room_id, user_id)

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
