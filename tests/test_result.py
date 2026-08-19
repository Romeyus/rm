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
