import peewee
from .models import Person, FuncPosition, WorkTask, Status


def get_all_workers():
    person = Person.select(Person, FuncPosition.title).join(FuncPosition)
    tasks = WorkTask.select(WorkTask, Status).join(Status).where(Status.state == 'В работе')
    return peewee.prefetch(person, tasks)


def get_all_tasks():
    return (
        WorkTask.select(
            WorkTask.id, WorkTask.equipment, WorkTask.title, WorkTask.article, WorkTask.order, WorkTask.deadline,
            WorkTask.duration,
            Status.state,
            Person.surname, Person.name, Person.second_name
        )
        .join(Status)
        .where(Status.state == 'В работе')
        .switch(WorkTask)
        .join(Person)
    )
            # .join(Person).dicts())

