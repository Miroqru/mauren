"""Общие исключение во время работы."""


class MauException(Exception):
    """Базовое исключение для всех ошибок работы с клиентом."""


class MauRequestError(MauException):
    """Ошибка во время отправки запроса."""

    def __init__(self, status_code: int, text: str) -> None:
        super().__init__(f"Server returned {status_code} status")
        self.status_code = status_code
        self.text = text
