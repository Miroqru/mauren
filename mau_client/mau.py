"""Главный класс для взаимодействия с сервером."""

from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from loguru import logger

from mau_client.enums import LeaderBoardGroups
from mau_client.exceptions import MauException
from mau_client.types.user import User

_DEFAULT_SERVER = "https://mau.miroq.ru/api/"


class Mau:
    """Взаимодействие с сервером."""

    def __init__(self, server: str = _DEFAULT_SERVER) -> None:
        self.server = server
        self.session = ClientSession(self.server)

    async def close(self) -> None:
        await self.session.close()

    async def _request(self, url: str, **options):
        try:
            async with self.session.get(
                url, headers=[("accept", "application/json")], **options
            ) as r:
                logger.debug("{} {}", url, r.status)

                if r.status == 200:
                    return await r.json()
                raise MauException(f"Server return {r.status} code")
        except ContentTypeError as e:
            raise MauException(f"Failed to parse: {e}")

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
