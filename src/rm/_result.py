from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

from rm._panic import Panic

type Result[T, E] = Ok[T, E] | Err[E, T]


@dataclass(frozen=True, slots=True)
class Ok[T, E = Any]:
    value: T

    def and_[U](self, result: Result[U, E]) -> Result[U, E]:
        return result

    def and_then[U](self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return func(self.value)

    def inspect(self, func: Callable[[T], Any]) -> Result[T, E]:
        func(self.value)
        return self

    def inspect_err(self, func: Callable[[E], Any]) -> Result[T, E]:
        return self

    def map[U](self, func: Callable[[T], U]) -> Result[U, E]:
        return Ok(func(self.value))

    def map_err[F](self, func: Callable[[E], F]) -> Result[T, F]:
        return cast(Result[T, F], self)

    def map_or[U](self, default: U, func: Callable[[T], U]) -> U:
        return func(self.value)

    def or_[F](self, result: Result[T, F]) -> Result[T, F]:
        return cast(Result[T, F], self)

    def or_else[F](self, func: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return cast(Result[T, F], self)

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> E:
        raise Panic(f"Called Result.unwrap_err() on an Ok value, {self.value}")


@dataclass(frozen=True, slots=True)
class Err[E, T = Any]:
    value: E

    def and_[U](self, result: Result[U, E]) -> Result[U, E]:
        return cast(Result[U, E], self)

    def and_then[U](self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return cast(Result[U, E], self)

    def inspect(self, func: Callable[[T], Any]) -> Result[T, E]:
        return self

    def inspect_err(self, func: Callable[[E], Any]) -> Result[T, E]:
        func(self.value)
        return self

    def map[U](self, func: Callable[[T], U]) -> Result[U, E]:
        return cast(Result[U, E], self)

    def map_err[F](self, func: Callable[[E], F]) -> Result[T, F]:
        return Err(func(self.value))

    def map_or[U](self, default: U, func: Callable[[T], U]) -> U:
        return default

    def or_[F](self, result: Result[T, F]) -> Result[T, F]:
        return result

    def or_else[F](self, func: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return func(self.value)

    def unwrap(self) -> T:
        raise Panic(f"Called Result.unwrap() on an Err value, {self.value}")

    def unwrap_err(self) -> E:
        return self.value
