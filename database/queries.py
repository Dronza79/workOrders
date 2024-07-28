import peewee
from .models import Person, FuncPosition, WorkTask, Status, WorkLapse


def get_all_workers():
    person = Person.select(Person, FuncPosition.title).join(FuncPosition)
    tasks = WorkTask.select(WorkTask, Status).join(Status).where(Status.state == 'В работе')
    # return peewee.prefetch(person, tasks)
    return (
        Person.select(
            Person.id, Person.surname, Person.name, Person.second_name,
            FuncPosition.title,
            WorkTask.order, WorkTask.deadline, peewee.fn.SUM(WorkLapse.term).alias('total'),
            Status.state,
        )
        .join_from(Person, FuncPosition)
        .join_from(Person, WorkTask, peewee.JOIN.LEFT_OUTER)
        .join_from(WorkTask, Status)
        .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
        .where(Status.state == 'В работе')
        .group_by(Person.id).dicts()
    )


def get_all_tasks():
    return (
        WorkTask.select(
            WorkTask.id, WorkTask.equipment, WorkTask.title, WorkTask.article, WorkTask.order,
            WorkTask.deadline, peewee.fn.SUM(WorkLapse.term).alias('total'),
            Status.state,
            Person.surname, Person.name, Person.second_name
        )
        .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
        .join_from(WorkTask, Status)
        .join_from(WorkTask, Person)
        .where(Status.state == 'В работе')
        .group_by(WorkTask.id).dicts()

        # WorkTask.select(
        #     WorkTask.id, WorkTask.equipment, WorkTask.title, WorkTask.article, WorkTask.order, WorkTask.deadline,
        #     WorkTask.duration,
        #     Status.state,
        #     Person.surname, Person.name, Person.second_name
        # )
        # .join(Status)
        # .where(Status.state == 'В работе')
        # .switch(WorkTask)
        # .join(Person)
    )



