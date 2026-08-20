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
