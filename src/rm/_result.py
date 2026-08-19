from dataclasses import dataclass
from typing import Any, cast

type Result[T, E] = Ok[T, E] | Err[E, T]


@dataclass(frozen=True, slots=True)
class Ok[T, E = Any]:
    value: T

    def and_[U](self, result: Result[U, E]) -> Result[U, E]:
        return result


@dataclass(frozen=True, slots=True)
class Err[E, T = Any]:
    value: E

    def and_[U](self, result: Result[U, E]) -> Result[U, E]:
        return cast(Result[U, E], self)
