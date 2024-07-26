import peewee
from .models import Person, FuncPosition, WorkTask


def get_all_workers():
    person = Person.select(Person, FuncPosition).join(FuncPosition)
    tasks = WorkTask.select()
    return peewee.prefetch(person, tasks)


def get_all_tasks():
    return WorkTask.select(WorkTask, Person).join(Person)
