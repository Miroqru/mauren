from pydantic import BaseModel, ConfigDict


class MauObject(BaseModel):
    """базовый класс для всех объектов API."""

    config = ConfigDict(frozen=True)
