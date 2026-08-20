from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar

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

    def filter(self, predicate: Callable[[T], bool]) -> Maybe[T]:
        return self if predicate(self.value) else Nothing

    def map[U](self, func: Callable[[T], U]) -> Maybe[U]:
        return Some(func(self.value))

    def map_or[U](self, default: U, func: Callable[[T], U]) -> U:
        return func(self.value)

    def map_or_else[U](self, default: Callable[[], U], func: Callable[[T], U]) -> U:
        return func(self.value)


class Nothing[T = Any]:
    value: ClassVar[None] = None

    @staticmethod
    def and_[U](maybe: Maybe[U]) -> Maybe[U]:
        return Nothing

    @staticmethod
    def and_then[U](func: Callable[[T], Maybe[U]]) -> Maybe[U]:
        return Nothing

    @staticmethod
    def expect(message: str) -> T:
        raise Panic(message)

    @staticmethod
    def filter(predicate: Callable[[T], bool]) -> Maybe[T]:
        return Nothing

    @staticmethod
    def map[U](func: Callable[[T], U]) -> Maybe[U]:
        return Nothing

    @staticmethod
    def map_or[U](default: U, func: Callable[[T], U]) -> U:
        return default

    @staticmethod
    def map_or_else[U](default: Callable[[], U], func: Callable[[T], U]) -> U:
        return default()
