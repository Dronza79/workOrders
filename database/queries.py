import peewee
from .models import Person, FuncPosition, WorkTask, Status


def get_all_workers():
    person = Person.select(Person, FuncPosition.title).join(FuncPosition)
    tasks = WorkTask.select(WorkTask, Status).join(Status).where(Status.name == 'В работе')
    return peewee.prefetch(person, tasks)


# def get_all_tasks():
#     return (WorkTask.select(WorkTask)
#             .join(Status).where(Status.name == 'В работе')
#             .switch(WorkTask).join(Person, peewee.JOIN.LEFT_OUTER).sql())
