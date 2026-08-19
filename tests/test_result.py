from unittest import mock

import rm


def test_value() -> None:
    """value should return the wrapped value"""
    ok = rm.Ok(0)
    assert ok.value == 0

    err = rm.Err("Some error message")
    assert err.value == "Some error message"


def test_and_() -> None:
    """and_ should return the input result if Ok and self if Err"""
    result_ok = rm.Ok("Input Ok result")
    result_err = rm.Err("Input Err result")

    ok = rm.Ok(0)
    assert ok.and_(result_ok) == result_ok
    assert ok.and_(result_err) == result_err

    err = rm.Err("Some error message")
    assert err.and_(result_ok) == err
    assert err.and_(result_err) == err


def test_and_then() -> None:
    """and_then should return the output result of the input function if Ok and self if Err"""

    def square_root(number: int) -> rm.Result[float, str]:
        if number < 0:
            return rm.Err("cannot square root a negative number")
        return rm.Ok(number**0.5)

    ok = rm.Ok(100)
    assert ok.and_then(square_root) == rm.Ok(10.0)

    err = rm.Err("Some error message")
    assert err.and_then(square_root) == err


def test_inspect() -> None:
    """inspect should be called once if Ok and should not be called if Err"""
    mock_func = mock.Mock()

    ok = rm.Ok(0)
    assert ok.inspect(mock_func) == ok
    mock_func.assert_called_once()

    mock_func.reset_mock()

    err = rm.Err("Some error message")
    assert err.inspect(mock_func) == err
    mock_func.assert_not_called()


def test_map() -> None:
    """map should return an Ok with the value of the applied function if Ok and self if Err"""

    def apply(message: str) -> str:
        return message.upper()

    ok = rm.Ok("Hello world")
    assert ok.map(apply) == rm.Ok("HELLO WORLD")

    err = rm.Err("Some error message")
    assert err.map(apply) == err


def test_map_err() -> None:
    """map_err should return self if Ok and an Err with the value of the applied function if Err"""

    def apply(message: str) -> str:
        return message.upper()

    ok = rm.Ok("Hello world")
    assert ok.map_err(apply) == ok

    err = rm.Err("Some error message")
    assert err.map_err(apply) == rm.Err("SOME ERROR MESSAGE")


def test_or_() -> None:
    """or_ should return self if Ok and the input result if Err"""
    result_ok = rm.Ok("Input Ok result")
    result_err = rm.Err("Input Err result")

    ok = rm.Ok("Original Ok result")
    assert ok.or_(result_ok) == ok
    assert ok.or_(result_err) == ok

    err = rm.Err("Some error message")
    assert err.or_(result_ok) == result_ok
    assert err.or_(result_err) == result_err


def test_or_else() -> None:
    """or_else should return self if Ok and the output result of the input function if Err"""

    def uppercase(message: str) -> rm.Result[str, str]:
        return rm.Err(message.upper())

    ok = rm.Ok("Original Ok result")
    assert ok.or_else(uppercase) == ok

    err = rm.Err("Some error message")
    assert err.or_else(uppercase) == rm.Err("SOME ERROR MESSAGE")
