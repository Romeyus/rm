from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar

from rm._panic import Panic
from rm._result import Err, Ok, Result

type Maybe[T] = Some[T] | type[Nothing[T]]


@dataclass(frozen=True, slots=True)
class Some[T]:
    value: T

    def and_[U](self, maybe: Maybe[U]) -> Maybe[U]:
        """
        If `self` if instance of `Some`, return `maybe`; else return `Nothing`.

        Note: `and_` is eagerly evaluated; for lazy evaluation, use `and_then`.
        """

        return maybe

    def and_then[U](self, func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """
        If `self` is instance of `Some`, return result of `func`; else return `Nothing`.
        """

        return func(self.value)

    def expect(self, message: str) -> T:
        """
        If `self` is instance of `Some`, return unwrapped value; else raise `Panic` with content of `message`.
        """

        return self.value

    def filter(self, predicate: Callable[[T], bool]) -> Maybe[T]:
        """
        If `self` if instance of `Some` and result of `predicate` is `True`, return `self`; else return `Nothing`.
        """

        return self if predicate(self.value) else Nothing

    def inspect(self, func: Callable[[T], Any]) -> Maybe[T]:
        """
        If `self` is instance of `Some`, call `func` once and return `self`; else return `Nothing`.
        """

        func(self.value)
        return self

    def map[U](self, func: Callable[[T], U]) -> Maybe[U]:
        """
        If `self` is instance of `Some`, return `Some[U]` where `U` is result of `func`; else return `Nothing`.
        """

        return Some(func(self.value))

    def map_or[U](self, default: U, func: Callable[[T], U]) -> U:
        """
        If `self` is instance of `Some`, return result of `func`; else return `default`.
        """

        return func(self.value)

    def map_or_else[U](self, default: Callable[[], U], func: Callable[[T], U]) -> U:
        """
        If `self` is instance of `Some`, return result of `func`; else return result of `default`.
        """

        return func(self.value)

    def ok_or[E](self, error: E) -> Result[T, E]:
        """
        If `self` is instance of `Some`, return `Ok[T]` where `T` is wrapped value; else return `Err[E]` where `E` is `error`.
        """

        return Ok(self.value)

    def ok_or_else[E](self, error: Callable[[], E]) -> Result[T, E]:
        """
        If `self` is instance of `Some`, return `Ok[T]` where `T` is wrapped value; else return `Err[E]` where `E` is result of `error`.
        """

        return Ok(self.value)

    def or_(self, maybe: Maybe[T]) -> Maybe[T]:
        """
        If `self` is instance of `Some`, return `self`; else return `maybe`.

        Note: `or_` is eagerly evaluated; for lazy evaluation, use `or_else`.
        """

        return self

    def or_else(self, func: Callable[[], Maybe[T]]) -> Maybe[T]:
        """
        If `self` is instance of `Some`, return `self`; else return result of `func`.
        """

        return self

    def unwrap(self) -> T:
        """
        If `self` is instance of `Some`, return unwrapped value; else raise `Panic`.
        """

        return self.value

    def unwrap_or(self, default: T) -> T:
        """
        If `self` is instance of `Some`, return unwrapped value; else return `default`.
        """

        return self.value

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        """
        If `self` is instance of `Some`, return unwrapped value; else return result of `default`.
        """

        return self.value


class Nothing[T = Any]:
    value: ClassVar[None] = None

    @staticmethod
    def and_[U](maybe: Maybe[U]) -> Maybe[U]:
        """
        If `self` if instance of `Some`, return `maybe`; else return `Nothing`.

        Note: `and_` is eagerly evaluated; for lazy evaluation, use `and_then`.
        """

        return Nothing

    @staticmethod
    def and_then[U](func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        """
        If `self` is instance of `Some`, return result of `func`; else return `self`.
        """

        return Nothing

    @staticmethod
    def expect(message: str) -> T:
        """
        If `self` is instance of `Some`, return unwrapped value; else raise `Panic` with content of `message`.
        """

        raise Panic(message)

    @staticmethod
    def filter(predicate: Callable[[T], bool]) -> Maybe[T]:
        """
        If `self` if instance of `Some` and result of `predicate` is `True`, return `self`; else return `Nothing`.
        """

        return Nothing

    @staticmethod
    def inspect(func: Callable[[T], Any]) -> Maybe[T]:
        """
        If `self` is instance of `Some`, call `func` once and return `self`; else return `Nothing`.
        """

        return Nothing

    @staticmethod
    def map[U](func: Callable[[T], U]) -> Maybe[U]:
        """
        If `self` is instance of `Some`, return `Some[U]` where `U` is result of `func`; else return `Nothing`.
        """

        return Nothing

    @staticmethod
    def map_or[U](default: U, func: Callable[[T], U]) -> U:
        """
        If `self` is instance of `Some`, return result of `func`; else return `default`.
        """

        return default

    @staticmethod
    def map_or_else[U](default: Callable[[], U], func: Callable[[T], U]) -> U:
        """
        If `self` is instance of `Some`, return result of `func`; else return result of `default`.
        """

        return default()

    @staticmethod
    def ok_or[E](error: E) -> Result[T, E]:
        """
        If `self` is instance of `Some`, return `Ok[T]` where `T` is wrapped value; else return `Err[E]` where `E` is `error`.
        """

        return Err(error)

    @staticmethod
    def ok_or_else[E](error: Callable[[], E]) -> Result[T, E]:
        """
        If `self` is instance of `Some`, return `Ok[T]` where `T` is wrapped value; else return `Err[E]` where `E` is result of `error`.
        """

        return Err(error())

    @staticmethod
    def or_(maybe: Maybe[T]):
        """
        If `self` is instance of `Some`, return `self`; else return `maybe`.

        Note: `or_` is eagerly evaluated; for lazy evaluation, use `or_else`.
        """

        return maybe

    @staticmethod
    def or_else(func: Callable[[], Maybe[T]]) -> Maybe[T]:
        """
        If `self` is instance of `Some`, return `self`; else return result of `func`.
        """

        return func()

    @staticmethod
    def unwrap() -> T:
        """
        If `self` is instance of `Some`, return unwrapped value; else raise `Panic`.
        """

        raise Panic("Called Maybe.unwrap() on a Nothing value")

    @staticmethod
    def unwrap_or(default: T) -> T:
        """
        If `self` is instance of `Some`, return unwrapped value; else return `default`.
        """

        return default

    @staticmethod
    def unwrap_or_else(default: Callable[[], T]) -> T:
        """
        If `self` is instance of `Some`, return unwrapped value; else return result of `default`.
        """

        return default()
