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
