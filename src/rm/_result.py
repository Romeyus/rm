from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

from rm._panic import Panic

type Result[T, E] = Ok[T, E] | Err[E, T]


@dataclass(frozen=True, slots=True)
class Ok[T, E = Any]:
    value: T

    def and_[U](self, result: Result[U, E]) -> Result[U, E]:
        """
        If `self` is instance of `Ok`, return `result`; else return `self`.

        Note: `and_` is eagerly evaluated; for lazy evaluation, use `and_then`.
        """

        return result

    def and_then[U](self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """
        If `self` is instance of `Ok`, return result of `func`; else return `self`.
        """

        return func(self.value)

    def expect(self, message: str) -> T:
        """
        If `self` is instance of `Ok`, return unwrapped value; else raise `Panic` with content of `message`.
        """

        return self.value

    def expect_err(self, message: str) -> E:
        """
        If `self` is instance of `Err`, return unwrapped value; else raise `Panic` with content of `message`.
        """

        raise Panic(message)

    def inspect(self, func: Callable[[T], Any]) -> Result[T, E]:
        """
        If `self` is instance of `Ok`, call `func` once; then return `self`.
        """

        func(self.value)
        return self

    def inspect_err(self, func: Callable[[E], Any]) -> Result[T, E]:
        """
        If `self` is instance of `Err`, call `func` once; then return `self`.
        """

        return self

    def map[U](self, func: Callable[[T], U]) -> Result[U, E]:
        """
        If `self` is instance of `Ok`, return `Ok[U]` where `U` is result of `func`; else return `self`.
        """

        return Ok(func(self.value))

    def map_err[F](self, func: Callable[[E], F]) -> Result[T, F]:
        """
        If `self` is instance of `Err`, return `Err[F]` where `F` is result of `func`; else return `self`.
        """

        return cast(Result[T, F], self)

    def map_or[U](self, default: U, func: Callable[[T], U]) -> U:
        """
        If `self` is instance of `Ok`, return result of `func`; else return `default`.
        """

        return func(self.value)

    def map_or_else[U](self, default: Callable[[E], U], func: Callable[[T], U]) -> U:
        """
        If `self` is instance of `Ok`, return result of `func`; else return result of `default`.
        """

        return func(self.value)

    def or_[F](self, result: Result[T, F]) -> Result[T, F]:
        """
        If `self` is instance of `Err`, return `result`; else return `self`.

        Note: `or_` is eagerly evaluated; for lazy evaluation, use `or_else`.
        """

        return cast(Result[T, F], self)

    def or_else[F](self, func: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """
        If `self` is instance of `Err`, return result of `func`; else return `self`.
        """

        return cast(Result[T, F], self)

    def unwrap(self) -> T:
        """
        If `self` is instance of `Ok`, return unwrapped value; else raise `Panic`.
        """

        return self.value

    def unwrap_err(self) -> E:
        """
        If `self` is instance of `Err`, return unwrapped value; else raise `Panic`.
        """

        raise Panic(f"Called Result.unwrap_err() on an Ok value, {self.value}")

    def unwrap_or(self, default: T) -> T:
        """
        If `self` is instance of `Ok`, return unwrapped value; else return `default`.
        """

        return self.value

    def unwrap_or_else(self, default: Callable[[E], T]) -> T:
        """
        If `self` is instance of `Ok`, return unwrapped value; else return result of `default`.
        """

        return self.value


@dataclass(frozen=True, slots=True)
class Err[E, T = Any]:
    value: E

    def and_[U](self, result: Result[U, E]) -> Result[U, E]:
        """
        If `self` is instance of `Ok`, return `result`; else return `self`.

        Note: `and_` is eagerly evaluated; for lazy evaluation, use `and_then`.
        """

        return cast(Result[U, E], self)

    def and_then[U](self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """
        If `self` is instance of `Ok`, return result of `func`; else return `self`.
        """

        return cast(Result[U, E], self)

    def expect(self, message: str) -> T:
        """
        If `self` is instance of `Ok`, return unwrapped value; else raise `Panic` with content of `message`.
        """

        raise Panic(message)

    def expect_err(self, message: str) -> E:
        """
        If `self` is instance of `Err`, return unwrapped value; else raise `Panic` with content of `message`.
        """

        return self.value

    def inspect(self, func: Callable[[T], Any]) -> Result[T, E]:
        """
        If `self` is instance of `Ok`, call `func` once; then return `self`.
        """

        return self

    def inspect_err(self, func: Callable[[E], Any]) -> Result[T, E]:
        """
        If `self` is instance of `Err`, call `func` once; then return `self`.
        """

        func(self.value)
        return self

    def map[U](self, func: Callable[[T], U]) -> Result[U, E]:
        """
        If `self` is instance of `Ok`, return `Ok[U]` where `U` is result of `func`; else return `self`.
        """

        return cast(Result[U, E], self)

    def map_err[F](self, func: Callable[[E], F]) -> Result[T, F]:
        """
        If `self` is instance of `Err`, return `Err[F]` where `F` is result of `func`; else return `self`.
        """

        return Err(func(self.value))

    def map_or[U](self, default: U, func: Callable[[T], U]) -> U:
        """
        If `self` is instance of `Ok`, return result of `func`; else return `default`.
        """

        return default

    def map_or_else[U](self, default: Callable[[E], U], func: Callable[[T], U]) -> U:
        """
        If `self` is instance of `Ok`, return result of `func`; else return result of `default`.
        """

        return default(self.value)

    def or_[F](self, result: Result[T, F]) -> Result[T, F]:
        """
        If `self` is instance of `Err`, return `result`; else return `self`.

        Note: `or_` is eagerly evaluated; for lazy evaluation, use `or_else`.
        """

        return result

    def or_else[F](self, func: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """
        If `self` is instance of `Err`, return result of `func`; else return `self`.
        """

        return func(self.value)

    def unwrap(self) -> T:
        """
        If `self` is instance of `Ok`, return unwrapped value; else raise `Panic`.
        """

        raise Panic(f"Called Result.unwrap() on an Err value, {self.value}")

    def unwrap_err(self) -> E:
        """
        If `self` is instance of `Err`, return unwrapped value; else raise `Panic`.
        """

        return self.value

    def unwrap_or(self, default: T) -> T:
        """
        If `self` is instance of `Ok`, return unwrapped value; else return `default`.
        """

        return default

    def unwrap_or_else(self, default: Callable[[E], T]) -> T:
        """
        If `self` is instance of `Ok`, return unwrapped value; else return result of `default`.
        """

        return default(self.value)
