from dataclasses import dataclass
from typing import Any, ClassVar

type Maybe[T] = Some[T] | type[Nothing[T]]


@dataclass(frozen=True, slots=True)
class Some[T]:
    value: T


class Nothing[T = Any]:
    value: ClassVar[None] = None
