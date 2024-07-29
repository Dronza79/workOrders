import peewee
from .models import Person, FuncPosition, WorkTask, Status, WorkLapse


def get_all_workers():
    return (
        Person.select(
            Person.id, Person.surname, Person.name, Person.second_name,
            FuncPosition.title.alias('post'),
            WorkTask.order, WorkTask.deadline, peewee.fn.SUM(WorkLapse.value).alias('total'),
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
            WorkTask.id, WorkTask.type_obj, WorkTask.title, WorkTask.article, WorkTask.order,
            WorkTask.deadline, peewee.fn.SUM(WorkLapse.value).alias('total'),
            Status.state,
            Person.surname, Person.name, Person.second_name,
            FuncPosition.title.alias('post')
        )
        .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
        .join_from(WorkTask, Status)
        .join_from(WorkTask, Person)
        .join_from(Person, FuncPosition)
        .where(Status.state == 'В работе')
        .group_by(WorkTask.id).dicts()
    )



