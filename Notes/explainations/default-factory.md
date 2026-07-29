The important distinction is:

* `default=` → use a fixed value.
* `default_factory=` → call a function to create a new value for each instance.

Your example has a small mistake.

### Incorrect

```python
created_at: datetime = field(default_factory=datetime.now())
```

Here, `datetime.now()` is **called immediately** when the class is defined, producing one `datetime` object.

It is effectively the same as:

```python
t = datetime.now()

created_at: datetime = field(default=t)
```

Every `Task` would get the **same timestamp**.

---

### Correct

Pass the function itself, not its result:

```python
created_at: datetime = field(default_factory=datetime.now)
```

Now, whenever a new `Task` is created, dataclasses execute:

```python
datetime.now()
```

so each instance gets its own creation time.

Example:

```python
from dataclasses import dataclass, field
from datetime import datetime
import time

@dataclass
class Task:
    created_at: datetime = field(default_factory=datetime.now)

t1 = Task()
time.sleep(2)
t2 = Task()

print(t1.created_at)
print(t2.created_at)
```

Output:

```
2026-07-29 13:55:10
2026-07-29 13:55:12
```

---

### When to use `default`

Use it when the value is immutable and the same for every instance.

```python
status: str = field(default="Todo")
priority: int = field(default=1)
active: bool = field(default=True)
```

These values never need to be generated.

---

### When to use `default_factory`

Use it when each instance needs a fresh value.

Examples:

```python
id: str = field(default_factory=lambda: str(uuid4()))

created_at: datetime = field(default_factory=datetime.now)

tags: list[str] = field(default_factory=list)

metadata: dict = field(default_factory=dict)

visited: set[str] = field(default_factory=set)
```

---

### Why not use `default=[]`?

Consider:

```python
@dataclass
class Task:
    tags: list[str] = []
```

Every instance would share the same list (and dataclasses reject this to prevent bugs).

Instead:

```python
@dataclass
class Task:
    tags: list[str] = field(default_factory=list)
```

Each instance gets its own empty list.

---

### Rule of thumb

* Known constant → `default=`

```python
status: str = field(default="Todo")
```

* Value must be computed or a new object is needed → `default_factory=`

```python
created_at: datetime = field(default_factory=datetime.now)
id: str = field(default_factory=lambda: str(uuid4()))
tags: list[str] = field(default_factory=list)
```

Notice that with `default_factory`, you pass a **callable** (`datetime.now`, `list`, `dict`), **not** the result of calling it (`datetime.now()`, `[]`, `{}`).
