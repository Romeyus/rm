from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Panic(BaseException):
    message: str
