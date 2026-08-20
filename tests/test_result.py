from unittest import mock

import pytest

import rm


def test_value() -> None:
    """Should return unwrapped value."""

    ok = rm.Ok(0)
    assert ok.value == 0

    err = rm.Err("Some error message")
    assert err.value == "Some error message"


def test_and_() -> None:
    """Should return `result` if `Ok` else `self`."""

    result_ok = rm.Ok("Input Ok result")
    result_err = rm.Err("Input Err result")

    ok = rm.Ok(0)
    assert ok.and_(result_ok) == result_ok
    assert ok.and_(result_err) == result_err

    err = rm.Err("Some error message")
    assert err.and_(result_ok) == err
    assert err.and_(result_err) == err


def test_and_then() -> None:
    """Should return result of `func` if `Ok` else `self`."""

    def square_root(number: int) -> rm.Result[float, str]:
        if number < 0:
            return rm.Err("cannot get square root of negative number")
        return rm.Ok(number**0.5)

    ok = rm.Ok(100)
    assert ok.and_then(square_root) == rm.Ok(10.0)

    ok = rm.Ok(-100)
    assert ok.and_then(square_root) == rm.Err(
        "cannot get square root of negative number"
    )

    err = rm.Err("Some error message")
    assert err.and_then(square_root) == err


def test_expect() -> None:
    """Should return unwrapped value if `Ok` else raises `Panic` with `message`."""

    ok = rm.Ok(0)
    assert ok.expect("My expect message") == 0

    err = rm.Err("Some error message")
    with pytest.raises(rm.Panic, match=r"My expect message"):
        err.expect("My expect message")


def test_expect_err() -> None:
    """Should return unwrapped value if `Err` else raises `Panic` with `message`."""

    ok = rm.Ok(0)
    with pytest.raises(rm.Panic, match=r"My expect message"):
        ok.expect_err("My expect message")

    err = rm.Err("Some error message")
    assert err.expect_err("My expect message") == "Some error message"


def test_inspect() -> None:
    """Should call `func` once if `Ok`. Always returns `self`."""

    mock_func = mock.Mock()

    ok = rm.Ok(0)
    assert ok.inspect(mock_func) == ok
    mock_func.assert_called_once()

    mock_func.reset_mock()

    err = rm.Err("Some error message")
    assert err.inspect(mock_func) == err
    mock_func.assert_not_called()


def test_inspect_err() -> None:
    """Should call `func` once if `Err`. Always returns `self`."""

    mock_func = mock.Mock()

    ok = rm.Ok(0)
    assert ok.inspect_err(mock_func) == ok
    mock_func.assert_not_called()

    mock_func.reset_mock()

    err = rm.Err("Some error message")
    assert err.inspect_err(mock_func) == err
    mock_func.assert_called_once()


def test_map() -> None:
    """Should return `Ok[U]`, where `U` is result of `func`, if `Ok` else `self`."""

    def apply(message: str) -> str:
        return message.upper()

    ok = rm.Ok("Hello world")
    assert ok.map(apply) == rm.Ok("HELLO WORLD")

    err = rm.Err("Some error message")
    assert err.map(apply) == err


def test_map_err() -> None:
    """Should return `Err[F]`, where `F` is result of `func`, if `Err` else `self`."""

    def apply(message: str) -> str:
        return message.upper()

    ok = rm.Ok("Hello world")
    assert ok.map_err(apply) == ok

    err = rm.Err("Some error message")
    assert err.map_err(apply) == rm.Err("SOME ERROR MESSAGE")


def test_map_or() -> None:
    """Should return result of `func` if `Ok` else `default`."""

    def apply(message: str) -> str:
        return message.upper()

    ok = rm.Ok("Hello world")
    assert ok.map_or("DEFAULT", apply) == "HELLO WORLD"

    err = rm.Err("Some error message")
    assert err.map_or("DEFAULT", apply) == "DEFAULT"


def test_map_or_else() -> None:
    """Should return result of `func` if `Ok` else result of `default`."""

    def apply(message: str) -> str:
        return message.upper()

    def apply_default(message: str) -> str:
        return message.lower()

    ok = rm.Ok("Hello world")
    assert ok.map_or_else(apply_default, apply) == "HELLO WORLD"

    err = rm.Err("Some error message")
    assert err.map_or_else(apply_default, apply) == "some error message"


def test_or_() -> None:
    """Should return `result` if `Err` else `self`."""

    result_ok = rm.Ok("Input Ok result")
    result_err = rm.Err("Input Err result")

    ok = rm.Ok("Original Ok result")
    assert ok.or_(result_ok) == ok
    assert ok.or_(result_err) == ok

    err = rm.Err("Some error message")
    assert err.or_(result_ok) == result_ok
    assert err.or_(result_err) == result_err


def test_or_else() -> None:
    """Should return result of `func` if `Err` else `self`."""

    def uppercase(message: str) -> rm.Result[str, str]:
        return rm.Err(message.upper())

    ok = rm.Ok("Original Ok result")
    assert ok.or_else(uppercase) == ok

    err = rm.Err("Some error message")
    assert err.or_else(uppercase) == rm.Err("SOME ERROR MESSAGE")


def test_unwrap() -> None:
    """Should return unwrapped value if `Ok` else raises `Panic`."""

    ok = rm.Ok(0)
    assert ok.unwrap() == 0

    err = rm.Err("Some error message")
    with pytest.raises(rm.Panic):
        err.unwrap()


def test_unwrap_err() -> None:
    """Should return unwrapped value if `Err` else raises `Panic`."""

    ok = rm.Ok(0)
    with pytest.raises(rm.Panic):
        ok.unwrap_err()

    err = rm.Err("Some error message")
    assert err.unwrap_err() == "Some error message"


def test_unwrap_or() -> None:
    """Should return unwrapped value if `Ok` else `default`."""

    ok = rm.Ok(0)
    assert ok.unwrap_or(1) == 0

    err = rm.Err("Some error message")
    assert err.unwrap_or(1) == 1


def test_unwrap_or_else() -> None:
    """Should return unwrapped value if `Ok` else result of `default`."""

    ok = rm.Ok(1)
    assert ok.unwrap_or_else(int) == 1

    err = rm.Err("123")
    assert err.unwrap_or_else(int) == 123
