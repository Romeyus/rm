from unittest import mock

import pytest

import rm


def test_value() -> None:
    """Should return the unwrapped value. `Nothing` should always return `None`."""

    some = rm.Some(0)
    assert some.value == 0

    assert rm.Nothing.value is None


def test_and_() -> None:
    """Should return `maybe` if `Some`; else `Nothing`."""

    some = rm.Some(0)
    assert some.and_(rm.Some(1)) == rm.Some(1)
    assert some.and_(rm.Nothing) == rm.Nothing

    assert rm.Nothing.and_(rm.Some(0)) == rm.Nothing
    assert rm.Nothing.and_(rm.Nothing) == rm.Nothing


def test_and_then() -> None:
    """Should return result of `func` if `Some`; else `Nothing`."""

    some = rm.Some(1)
    assert some.and_then(lambda v: rm.Some(v * 2)) == rm.Some(2)
    assert some.and_then(lambda _: rm.Nothing) == rm.Nothing

    assert rm.Nothing.and_then(lambda v: rm.Some(v + 1)) == rm.Nothing
    assert rm.Nothing.and_then(lambda _: rm.Nothing) == rm.Nothing


def test_expect() -> None:
    """Should return unwrapped value if `Some`; else raises `Panic` with content `message`."""

    some = rm.Some(0)
    assert some.expect("my expect message") == 0

    with pytest.raises(rm.Panic, match=r"my expect message"):
        rm.Nothing.expect("my expect message")


def test_filter() -> None:
    """Should return `self` if `Some` and result of `predicate` is `True`; else `Nothing`."""

    def is_even(x: int) -> bool:
        return x % 2 == 0

    assert rm.Some(4).filter(is_even) == rm.Some(4)
    assert rm.Some(3).filter(is_even) == rm.Nothing
    assert rm.Nothing.filter(is_even) == rm.Nothing


def test_inspect() -> None:
    """Should call `func` once if `Some`; else should not call `func`."""

    mock_func = mock.Mock()

    rm.Some(0).inspect(mock_func)
    mock_func.assert_called_once()

    mock_func.reset_mock()

    rm.Nothing.inspect(mock_func)
    mock_func.assert_not_called()


def test_map() -> None:
    """Should return `Some[U], where `U` is result of `func`, if `Some`; else `Nothing`."""

    def uppercase(message: str) -> str:
        return message.upper()

    assert rm.Some("hello world").map(uppercase) == rm.Some("HELLO WORLD")
    assert rm.Nothing.map(uppercase) == rm.Nothing


def test_map_or() -> None:
    """Should return result of `func` if `Some`; else `default`."""

    def uppercase(message: str) -> str:
        return message.upper()

    assert rm.Some("hello world").map_or("DEFAULT", uppercase) == "HELLO WORLD"
    assert rm.Nothing.map_or("DEFAULT", uppercase) == "DEFAULT"


def test_map_or_else() -> None:
    """Should return result of `func` if `Some`; else result of `default`."""

    def apply(message: str) -> str:
        return message.upper()

    def apply_default() -> str:
        return "DEFAULT"

    assert rm.Some("hello world").map_or_else(apply_default, apply) == "HELLO WORLD"
    assert rm.Nothing.map_or_else(apply_default, apply) == "DEFAULT"


def test_ok_or() -> None:
    """Should return `Ok` with the wrapped value if `Some`; else `Err` with `error`."""

    assert rm.Some(0).ok_or("missing value") == rm.Ok(0)
    assert rm.Nothing.ok_or("missing value") == rm.Err("missing value")


def test_ok_or_else() -> None:
    """Should return `Ok` with the wrapped value if `Some`; else `Err` with the result of `error`."""

    def error() -> str:
        return "missing value"

    assert rm.Some(0).ok_or_else(error) == rm.Ok(0)
    assert rm.Nothing.ok_or_else(error) == rm.Err("missing value")


def test_or_() -> None:
    """Should return `self` if `Some`; else `maybe`."""

    assert rm.Some(0).or_(rm.Some(1)) == rm.Some(0)
    assert rm.Some(0).or_(rm.Nothing) == rm.Some(0)
    assert rm.Nothing.or_(rm.Some(0)) == rm.Some(0)


def test_or_else() -> None:
    """Should return `self` if `Some`; else result of `func`."""

    assert rm.Some(0).or_else(lambda: rm.Some(1)) == rm.Some(0)
    assert rm.Some(0).or_else(lambda: rm.Nothing) == rm.Some(0)
    assert rm.Nothing.or_else(lambda: rm.Some(0)) == rm.Some(0)


def test_unwrap() -> None:
    """Should return unwrapped value if `Some`; else raises `Panic`."""

    assert rm.Some(0).unwrap() == 0

    with pytest.raises(rm.Panic):
        rm.Nothing.unwrap()


def test_unwrap_or() -> None:
    """Should return unwrapped value if `Some`; else `default`."""

    assert rm.Some(0).unwrap_or(1) == 0
    assert rm.Nothing.unwrap_or(1) == 1


def test_unwrap_or_else() -> None:
    """Should return unwrapped value if `Some`; else result of `default`."""

    assert rm.Some(0).unwrap_or_else(lambda: 1) == 0
    assert rm.Nothing.unwrap_or_else(lambda: 1) == 1
