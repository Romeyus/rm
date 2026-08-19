from dataclasses import dataclass
from typing import Any

type Result[T, E] = Ok[T, E] | Err[E, T]


@dataclass(frozen=True, slots=True)
class Ok[T, E = Any]:
    value: T


@dataclass(frozen=True, slots=True)
class Err[E, T = Any]:
    value: E
