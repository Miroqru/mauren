"""Главный класс для взаимодействия с сервером."""

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from loguru import logger

from mauren.enums import LeaderBoardGroups
from mauren.exceptions import MauException, MauRequestError
from mauren.types.context import GameContext
from mauren.types.game import CardColor
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

    # Game
    # ====

    async def join_game(self, token: str) -> GameContext:
        """Добавляет пользователя в игру."""
        res = await self._request(
            "/game/join", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    async def leave_game(self, token: str) -> GameContext:
        """Покинуть игру."""
        res = await self._request(
            "/game/leave", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    async def active_game(self, token: str) -> GameContext:
        """Возвращает актуальный игровой контекст."""
        res = await self._request(
            "/game/", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    async def start_game(self, token: str) -> GameContext:
        """Начинает игру в комнате."""
        res = await self._request(
            "/game/start", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    async def end_game(self, token: str) -> GameContext:
        """Принудительно завершает игру в комнате."""
        res = await self._request(
            "/game/end", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    # Game actions
    # ============

    async def game_kick(self, token: str, user_id: str) -> GameContext:
        """Выгоняет игрока из игры."""
        res = await self._request(
            f"/game/kick/{user_id}",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return GameContext.validate(res)

    async def game_skip(self, token: str) -> GameContext:
        """Пропускает текущего игрока в игре."""
        res = await self._request(
            "/game/skip", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    async def game_next(self, token: str) -> GameContext:
        """Передаёт ход следующему игроку."""
        res = await self._request(
            "/game/next", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    async def game_take(self, token: str) -> GameContext:
        """Берёт карты."""
        res = await self._request(
            "/game/tale", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    async def game_shotgun_take(self, token: str) -> GameContext:
        """Берёт карты вместо выстрела из револьвера."""
        res = await self._request(
            "/game/shotgun/take",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return GameContext.validate(res)

    async def game_shotgun_shot(self, token: str) -> GameContext:
        """Выстреливает из револьвера вместо взятия карт."""
        res = await self._request(
            "/game/shotgun/shot",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return GameContext.validate(res)

    async def game_bluff(self, token: str) -> GameContext:
        """Проверяет прошлого игрока на честность."""
        res = await self._request(
            "/game/bluff", method="post", headers=[("Authorization", f"Bearer {token}")]
        )
        return GameContext.validate(res)

    async def game_color(self, token: str, color: CardColor) -> GameContext:
        """Выбирает цвет для карты."""
        res = await self._request(
            f"/game/color/{color.value}",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return GameContext.validate(res)

    async def game_player(self, token: str, user_id: str) -> GameContext:
        """Выбирает игрока для обмена картами."""
        res = await self._request(
            f"/game/player/{user_id}",
            method="post",
            headers=[("Authorization", f"Bearer {token}")],
        )
        return GameContext.validate(res)

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
