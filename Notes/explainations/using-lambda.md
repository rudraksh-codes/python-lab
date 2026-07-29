`uuid4()` generates a **Universally Unique Identifier (UUID)**.

A UUID is a 128-bit random identifier designed to be unique across machines, processes, and time with an extremely low chance of collision.

Example:

```python id="smu8e2"
from uuid import uuid4

print(uuid4())
```

Output:

```text
550e8400-e29b-41d4-a716-446655440000
```

Since `uuid4()` returns a `UUID` object, not a string:

```python id="3mg5y4"
from uuid import uuid4

id = uuid4()

print(id)
print(type(id))
```

Output:

```text
550e8400-e29b-41d4-a716-446655440000
<class 'uuid.UUID'>
```

---

## Why `str(uuid4())`?

Your field is annotated as:

```python id="svq4gt"
id: str
```

so you convert the UUID object to a string:

```python id="w2tkmo"
str(uuid4())
```

Result:

```text
"550e8400-e29b-41d4-a716-446655440000"
```

---

## Why `default_factory`?

Just like `datetime.now`, you want a **new UUID for every instance**.

Correct:

```python id="gm2d65"
id: str = field(default_factory=lambda: str(uuid4()))
```

Each new `Task` gets its own random ID.

---

## Can I do this?

No:

```python id="gq5zsp"
id: str = field(default_factory=str(uuid4()))
```

This is wrong because `str(uuid4())` is executed **once**, immediately.

Suppose it generated:

```text
"abc123"
```

Then every `Task` would get:

```python id="tkgftm"
id = "abc123"
```

which defeats the purpose of a unique identifier.

---

## Why use `lambda`?

`default_factory` expects **a callable that takes no arguments**.

Its signature is conceptually:

```python id="84b08s"
default_factory: Callable[[], Any]
```

The lambda is simply a zero-argument function:

```python id="3c3v6w"
lambda: str(uuid4())
```

When dataclasses need a default value, they call it:

```python id="ymzj5q"
lambda: str(uuid4())
```

producing a fresh string each time.

---

## Can I write `default_factory=uuid4`?

Yes, if the field type is `UUID`:

```python id="zrklig"
from uuid import UUID, uuid4

id: UUID = field(default_factory=uuid4)
```

No lambda is needed because `uuid4` is already a zero-argument callable.

---

## Why is lambda needed here?

Because you need **two operations**:

1. Generate a UUID.
2. Convert it to a string.

`default_factory` can only call **one callable**, so you wrap both steps in a lambda:

```python id="34mbie"
lambda: str(uuid4())
```

---

Another option is to define a regular function instead of a lambda:

```python id="f7q3v8"
from uuid import uuid4

def generate_id() -> str:
    return str(uuid4())

id: str = field(default_factory=generate_id)
```

This is functionally identical. Many teams prefer a named function if the factory logic becomes more complex; for a one-line conversion like this, a lambda is common and concise.
