
from datetime import datetime, timedelta

from project.models.task import Task
from project.models.project import Project

project = Project(
    id="P001",
    name="ProjectFlow"
)

task1 = Task(
    title="Authentication",
    status="Todo",
    assignee="Alice",
    due_date=datetime.now() + timedelta(days=2)
)

task2 = Task(
    title="API Development",
    status="Completed",
    assignee="Bob",
    due_date=datetime.now() + timedelta(days=4)
)

task3 = Task(
    title="Testing",
    status="Todo",
    assignee="Alice",
    due_date=datetime.now() + timedelta(days=6)
)

project.add_task(task1)
project.add_task(task2)
project.add_task(task3)

print(project)
print(project.task_count)