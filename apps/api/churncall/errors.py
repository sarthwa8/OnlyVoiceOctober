"""Domain errors. Use cases raise these; churncall.api maps each one to an HTTP status in one place."""

from __future__ import annotations


class ChurnCallError(Exception):
    """Base class. The message is safe to show to the caller."""


class InviteNotFound(ChurnCallError):
    def __init__(self) -> None:
        super().__init__("unknown invite")


class InviteFinished(ChurnCallError):
    def __init__(self) -> None:
        super().__init__("this invite is already finished")


class TooManyAttempts(ChurnCallError):
    def __init__(self) -> None:
        super().__init__("too many attempts for this invite")


class ConsentRequired(ChurnCallError):
    def __init__(self) -> None:
        super().__init__("consent required: the user must request the call")


class InvalidPhone(ChurnCallError):
    def __init__(self) -> None:
        super().__init__("phone number must include the country code, e.g. +919800000000")


class BolnaUnavailable(ChurnCallError):
    """Bolna refused or couldn't be reached. `status` is Bolna's HTTP status when it should be passed
    through to the caller (the Web Call SDK reads e.g. 429 as "at capacity"); None means 502."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status
