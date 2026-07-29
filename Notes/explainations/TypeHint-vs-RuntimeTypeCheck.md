Use the class itself, **not a string**.

Correct:

```python
def __eq__(self, other: object) -> bool:
    return isinstance(other, Task) and self.id == other.id
```

Not:

```python
def __eq__(self, other: object) -> bool:
    return isinstance(other, "Task") and self.id == other.id
```

The second version is invalid because `isinstance()` expects a **type**, a tuple of types, or a union—not a string.

For example:

```python
isinstance(x, int)      # ✅
isinstance(x, str)      # ✅
isinstance(x, (int, str))  # ✅
isinstance(x, "Task")   # ❌ TypeError
```

### Why can you refer to `Task` inside its own class?

When the method is executed, the class has already been created, so `Task` is defined.

```python
@dataclass(eq=False)
class Task:
    ...

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Task) and self.id == other.id
```

This works without any issue.

### What about string annotations?

You may have seen this:

```python
@classmethod
def quick_task(cls) -> "Task":
    ...
```

or on older Python versions:

```python
def copy(self) -> "Task":
    ...
```

The string is used **only in type annotations** (historically to avoid forward-reference issues). It is **not** used by runtime functions like `isinstance()`.

So:

```python
def clone(self) -> "Task":   # ✅ valid type annotation
    ...

isinstance(obj, Task)        # ✅ valid runtime check
isinstance(obj, "Task")      # ❌ invalid
```

On Python 3.11+, or if you use `from __future__ import annotations`, you can usually write return types directly as `Task` instead of `"Task"`.
