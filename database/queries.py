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


def get_worker_data(idx=None):
    if idx:
        person = (
            Person.select(Person, FuncPosition)
            .join_from(Person, FuncPosition)
            .where(Person.id == idx)
        )
        tasks = (
            WorkTask.select(
                WorkTask, Status, peewee.fn.SUM(WorkLapse.value).alias('total'))
            .join_from(WorkTask, Status)
            .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
            .order_by(WorkTask.status)
            .group_by(WorkTask.id)
        )
        worker = peewee.prefetch(person, tasks).pop()
    else:
        worker = None
    print(f'query = {worker=}')
    return {
        'func_position': FuncPosition.select(),
        'person': worker,
    }


def get_all_tasks():
    return (
        WorkTask.select(
            WorkTask.id, WorkTask.type_obj, WorkTask.title, WorkTask.article, WorkTask.order,
            WorkTask.deadline, peewee.fn.SUM(WorkLapse.value).alias('total'),
            Status.state,
            Person.surname, Person.name, Person.second_name, Person.table_num,
            FuncPosition.job_name.alias('post'), FuncPosition.id
        )
        .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
        .join_from(WorkTask, Status)
        .join_from(WorkTask, Person)
        .join_from(Person, FuncPosition)
    )


# @add_logger_peewee
def get_close_tasks():
    return (
        get_all_tasks()
        .where(Status.state == sv[2])
        .group_by(WorkTask.id)
    )


# @add_logger_peewee
def get_mounter_tasks():
    return (
        get_all_tasks()
        .where(
            Status.state != sv[2],
            Person.function.job_name.in_([fv[1], fv[2]])
        )
        .group_by(WorkTask.id)
    )


# @add_logger_peewee
def get_fitter_tasks():
    return (
        get_all_tasks()
        .where(
            Status.state != sv[2],
            Person.function.job_name.in_([fv[3], fv[4]])
        )
        .group_by(WorkTask.order)
    )
