import peewee
from .models import Person, FuncPosition, WorkTask, Status, WorkLapse, STATUS_VARIABLES as sv, FUNC_VARIABLES as fv


def get_all_workers():
    persons = (
        Person.select(Person.id, Person.surname, Person.name, Person.second_name, FuncPosition.job_name)
        .join(FuncPosition).group_by(Person.id)
    )
    tasks = (
        WorkTask.select(WorkTask, Status, peewee.fn.SUM(WorkLapse.value).alias('total'))
        .join_from(WorkTask, Status).join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
        .where(Status.state != sv[2])
        .order_by(WorkLapse.create_at)
        # .order_by(WorkLapse.create_at.desc())
        .group_by(WorkTask.id)
    )
    return peewee.prefetch(persons, tasks)
    # return (
    #     Person.select(
    #         Person.id, Person.surname, Person.name, Person.second_name,
    #         FuncPosition.title.alias('post'),
    #         WorkTask.order, WorkTask.deadline, peewee.fn.SUM(WorkLapse.value).alias('total'),
    #         Status.state,
    #     )
    #     .join_from(Person, FuncPosition)
    #     .join_from(Person, WorkTask, peewee.JOIN.LEFT_OUTER)
    #     .join_from(WorkTask, Status)
    #     .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
    #     .where(Status.state == 'В работе')
    #     .group_by(Person.id)
    #     # .dicts()
    # )


def get_all_tasks():
    return (
        WorkTask.select(
            WorkTask.id, WorkTask.type_obj, WorkTask.title, WorkTask.article, WorkTask.order,
            WorkTask.deadline, peewee.fn.SUM(WorkLapse.value).alias('total'),
            Status.state,
            Person.surname, Person.name, Person.second_name, Person.table_num,
            FuncPosition.job_name.alias('post')
        )
        .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
        .join_from(WorkTask, Status)
        .join_from(WorkTask, Person)
        .join_from(Person, FuncPosition)
    )


def get_close_tasks():
    return (
        get_all_tasks()
        .where(Status.state == sv[2])
        .group_by(WorkTask.id)
    )


def get_mounter_tasks():
    return (
        get_all_tasks()
        .where(
            Status.state != sv[2],
            Person.function.in_([fv[1], fv[2]])
        )
        .order_by(Person.function.id)
        .group_by(WorkTask.id)
    )


def get_fitter_tasks():
    return (
        get_all_tasks()
        .where(
            Status.state != sv[2],
            Person.function.in_([fv[3], fv[4]])
        )
        .group_by(WorkTask.order)
    )
