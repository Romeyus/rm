# rm

Provides the `Result` and `Maybe` monads for effective functional programming.

## Installation

With uv (recommended):

```bash
uv add rm
```

With pip:

```bash
pip install rm
```

## Examples

### Result

```python
import rm

def divide(a: float, b: float) -> rm.Result[float, str]:
    if b == 0:
        return rm.Err("cannot divide by zero")
    return rm.Ok(a / b)


ok_value = (
    divide(8, 2)
    .map(lambda v: v**2)
    .unwrap_or(5)
)
print(value) #> 16

err_value = divide(10, 0).unwrap_or(5)
print(value) #> 5
```

### Maybe

```python
import rm

users: dict[int, str] = {
    0: "Luke",
    1: "Leia",
    2: "Han"
}

def get_user(id: int) -> rm.Maybe[str]:
    user = users.get(id)
    if user is None:
        return rm.Nothing
    return rm.Some(user)


some_value = (
    get_user(0)
    .map(lambda v: v.upper())
    .unwrap_or("VADER")
)
print(some_value) #> LUKE

nothing_value = (
    get_user(10)
    .map(lambda v: v.lower())
    .unwrap_or("vader")
)
print(nothing_value) #> vader
```
