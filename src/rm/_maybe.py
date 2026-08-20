from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar, cast

from rm._panic import Panic

type Maybe[T] = Some[T] | type[Nothing[T]]


@dataclass(frozen=True, slots=True)
class Some[T]:
    value: T

    def and_[U](self, maybe: Maybe[U]) -> Maybe[U]:
        return maybe

    def and_then[U](self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return func(self.value)

    def expect(self, message: str) -> T:
        return self.value


class Nothing[T = Any]:
    value: ClassVar[None] = None

    @classmethod
    def and_[U](cls, maybe: Maybe[U]) -> Maybe[U]:
        return cast(Maybe[U], cls)

    @classmethod
    def and_then[U](cls, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return cast(Maybe[U], cls)

    @staticmethod
    def expect(message: str) -> T:
        raise Panic(message)
