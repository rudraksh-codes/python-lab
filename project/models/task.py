from dataclasses import dataclass, field
from datetime import datetime, timedelta


from uuid import uuid4

@dataclass(eq=False)
class Task:
    """
    Represents a single task in ProjectFlow.

    Business rules:

    - title cannot be empty
    - status must be valid
    - due_date cannot be before creation
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    title: str = ""

    description: str = ""

    status: str = "Todo"

    assignee: str | None = None

    created_at: datetime = field(default_factory=datetime.now) #fresh value for every instance

    due_date: datetime | None = None 

    priority: int = 3 

    tags: list[str] = field(default_factory=list)


    #validation
    def __post_init__(self):

        self.title = self.title.strip() 

        if not self.title:
            raise ValueError("Task title cannot be empty.")

        if self.status not in self.VALID_STATUS:
            raise ValueError(
                f"Invalid status: {self.status}"
            )

        if not (1 <= self.priority <= 5) : 
            raise ValueError(
                "Priority must be between 1 and 5"
            )

        if self.due_date:

            if self.due_date < self.created_at:
                raise ValueError(
                    "Due date cannot be before creation."
                )

    #property
    @property
    def is_overdue(self) -> bool: 
        """
        - task is not completed
        - due date exists
        - due date has passed
        """
        if self.status == "Completed":
            return False

        if self.due_date is None:
            return False 

        return datetime.now() > self.due_date

    #business methods 
    def mark_completed(self) -> None: 
        self.status = "Completed" 

    def assign_to(self, username: str) -> None: 
        self.assignee = username

    def postpone(self, days: int) -> None:

        if self.due_date:
            self.due_date += timedelta(days=days)

    #factory method 
    @classmethod
    def quick_task(
        cls, 
        title: str, 
        assignee: str 
    ) -> Task:
        """
        create a simple todo task.

        Factory methods provide readable construction
        for common use cases.
        """

        return cls(
            title = title, 
            assignee = assignee,
            status = "Todo"
        )


    #static utility 
    @staticmethod
    def valid_priority(priority: int) -> bool:
        """
        Static method dont require object state.
        """

        return 1 <= priority <= 5


    #dunder/magic methods
    def __str__(self) -> str:

        return(
            f"{self.title}"
            f"({self.status})"
        )

    def __repr__(self) -> str : 

        return(
            "Task("
            f"id='{self.id}', "
            f"title='{self.title}', "
            f"status='{self.status}'"
            ")"
        )

    def __eq__(self, other: object) -> bool: #Task is valid as the other object is already defined...
        return isinstance(other, Task) and self.id == other.id


    def __hash__(self) -> int:
        return hash(self.id)


    def __len__(self) -> int:
        """
        Length equals title length.
        """

        return len(self.title) 





#recurring task
@dataclass(eq=False)
class RecurringTask(Task):
    """
    Represents tasks that repeat automatically.

    Examples:

    - Daily Backup
    - Weekly Sprint Review
    - Monthly Invoice
    """

    recurrence_days: int = 7 

    def __post_init__(self):
        super().__post_init__() #using as Task._post_init__(), bound to the child object(self) already

        if self.recurrence_days <= 0:
            raise ValueError(
                "recurrence days must be positive."
            )

    def next_occurence(self) -> datetime:

        if self.due_date:
            return self.due_date + timedelta(
                days=self.recurrence_days
            )

        return datetime.now() + timedelta(
            days=self.recurrence_days
        )

    def __str__(self) -> str: 

        return (
            f"{self.title} "
            f"(Every {self.recurrence_days} days)"
        )


    def __repr__(self):
        return (
            "RecurringTask("
            f"title='{self.title}', "
            f"recurrence_days={self.recurrence_days}"
            ")"
        )