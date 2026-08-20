from dataclasses import dataclass
from typing import Any, ClassVar, cast

type Maybe[T] = Some[T] | type[Nothing[T]]


@dataclass(frozen=True, slots=True)
class Some[T]:
    value: T

    def and_[U](self, maybe: Maybe[U]) -> Maybe[U]:
        return maybe


class Nothing[T = Any]:
    value: ClassVar[None] = None

    @classmethod
    def and_[U](cls, maybe: Maybe[U]) -> Maybe[U]:
        return cast(Maybe[U], cls)
