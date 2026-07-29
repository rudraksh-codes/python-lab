No. You **do not** pass `self`.

Correct:

```python
super().__post_init__()
```

Not:

```python
super().__post_init__(self)
```

### Why?

When you access a method through an instance, Python creates a **bound method**.

Suppose you have:

```python
class Base:
    def __post_init__(self):
        print(self)
```

and

```python
class Child(Base):
    def __post_init__(self):
        super().__post_init__()
```

`super().__post_init__` is already bound to the current instance (`self`).

Internally, Python is effectively doing:

```python
Base.__post_init__(self)
```

So `self` is supplied automatically.

---

### It's the same as normal methods

For example:

```python
class Person:
    def greet(self):
        print("Hello")
```

You call:

```python
p = Person()
p.greet()
```

not

```python
p.greet(p)   # ❌
```

because `p.greet` is a bound method.

The same applies to:

```python
super().__post_init__()
```

---

### If you called the base class directly

Then you would have to pass `self` yourself:

```python
class Child(Base):
    def __post_init__(self):
        Base.__post_init__(self)
```

Here you're calling the function on the class, so Python does **not** automatically provide the instance.

---

### Summary

| Call                 | Pass `self`? |
| -------------------- | ------------ |
| `self.method()`      | No           |
| `super().method()`   | No           |
| `Class.method(self)` | Yes          |

So your code is correct:

```python
def __post_init__(self):
    super().__post_init__()

    if self.recurrence_days <= 0:
        raise ValueError("recurrence days must be positive.")
```

`super().__post_init__()` already invokes the parent class's `__post_init__` with the current instance.
