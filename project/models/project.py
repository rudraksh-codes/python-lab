from dataclasses import dataclass, field
from datetime import datetime
from project.models.task import Task #-- is this fine ? 
# from .task import Task, TaskNotFoundError
from collections import deque, defaultdict, Counter

@dataclass(eq=False)
class Project:
    """
    Represents a project consisting of multiple tasks.

    Composition :
        Project has a collection of Task obj.
    """

    id: str 

    name: str 

    description: str = "" 

    owner: str | None = None 

    created_at: datetime = field(default_factory=datetime.now)

    tasks: list[Task] = field(default_factory=list) 

    recent_activity: deque = field(
        default_factory= lambda: deque(maxlen=10)
    )

    #validation 

    def __post_init__(self):
        self.name = self.name.strip()

        if not self.name:
            raise ValueError("Project name cannot be empty")


    #Properties 
    @property
    def task_count(self) -> int:
        """
        Total number of tasks.
        """

        return len(self.tasks)



    #Business methods 
    def add_task(self, task: Task) -> None:

        self.tasks.append(task)

        self.recent_activity.append(
            f"Added '{task.title}'"
        )

    def get_task(self, task_id: str) -> Task:

        for task in self.tasks:
            if task.id == task_id:
                return task 

        raise TaskNotFoundError(
            f"No task found with id {task_id}"
        )


    def remove_task(self, task_id: str) -> None:

        task = self.get_task(task_id)
        self.tasks.remove(task)

        self.recent_activity.append(
            f"Removed '{task.title}'"
        )


    def complete_task(self, task_id: str) -> None:

        task = self.get_task()

        task.mark_completed() 

        self.recent_activity.append(
            f"Completed '{task.title}'"
        )


    #defaultdict demo 
    def group_tasks_by_status(self):

        grouped = defaultdict(list)

        for task in self.tasks:
            grouped[task.status].append(task)

        return grouped

    #counter demo 
    def status_statastics(self):
        #counter got a generator as count on the go instead 
        # of making a list in memory first
        return Counter(
            task.status
            for task in self.tasks
        )

    #list comprehension 
    def completed_tasks(self):
        return [
            task
            for task in self.tasks 
            if task.status == "Completed"
        ]


    #dict comprehension 
    def priority_lookup(self):
        return {
            task.title: task.priority
            for task in self.tasks
        }


    #set comprehension 
    def unique_assignees(self):
        return {
            task.assignee
            for task in self.tasks
            if task.assignee
        }

    #string slicing demo
    def short_code(self):

        """
        Return first three letters of project.

        Example

        ProjectFlow

        -> PRO
        """

        return self.name[:3].upper() 


    #dunder methods
    def __len__(self):
        return len(self.tasks)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: object):
        return isinstance(other, Project) and self.id == other.id

    def __str__(self):
        return(
            f"Project: {self.name} | "
            f"{self.task_count} Tasks"
        )

    def __repr__(self):

        return (
            "Project("
            f"id='{self.id}', "
            f"name='{self.name}', "
            f"tasks={self.task_count}"
            ")"
        )


