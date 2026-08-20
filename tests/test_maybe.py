import rm


def test_value() -> None:
    """Should return the unwrapped value. `Nothing` should always return `None`."""

    some = rm.Some(0)
    assert some.value == 0

    assert rm.Nothing.value is None
