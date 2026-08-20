from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar, cast

type Maybe[T] = Some[T] | type[Nothing[T]]


@dataclass(frozen=True, slots=True)
class Some[T]:
    value: T

    def and_[U](self, maybe: Maybe[U]) -> Maybe[U]:
        return maybe

    def and_then[U](self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return func(self.value)


class Nothing[T = Any]:
    value: ClassVar[None] = None

    @classmethod
    def and_[U](cls, maybe: Maybe[U]) -> Maybe[U]:
        return cast(Maybe[U], cls)

    @classmethod
    def and_then[U](cls, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return cast(Maybe[U], cls)
