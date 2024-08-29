import peewee

from .models import (
    Worker, Vacancy, Task, Status, Period, Order,
    STATUS_VARIABLES as sv,
    FUNC_VARIABLES as fv,
)


def get_all_workers():
    persons = (
        Worker
        .select(Worker.id, Worker.surname, Worker.name, Worker.second_name, Vacancy.post)
        .join(Vacancy).where(Worker.is_active == True)
    )

    periods = (
        Period
        .select(Period, Task, Order, Worker)
        .join_from(Period, Task)
        .join_from(Period, Order)
        .join_from(Period, Worker)
        .where(Task.status_id != 2)
        .order_by(Period.date)
        .group_by(Period.id)
    )
    tasks = (
        Task.select(Task, Worker, Order, Status, peewee.fn.SUM(Period.value).alias('total_time'))
        .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
        .join_from(Task, Order)
        .join_from(Task, Worker)
        .join_from(Task, Status)
        .group_by(Task.id)
    )
    return peewee.prefetch(persons, periods, tasks)


def get_all_orders():
    orders = (
        Order.select()
        .where(
            Order.order.not_in(Task.select(Task.order)) |
            Order.order.in_(Task.select(Task.order).join(Status).where(Task.status.state.in_([sv[1], sv[3]])))
        )
        .group_by(Order.order)
    )

    tasks = (
        Task.select(Task, Worker.surname, Worker.name, Worker.second_name)
        .join_from(Task, Worker)
        .group_by(Task.id)
    )

    return peewee.prefetch(orders, tasks)


def get_worker_data(idx=None):
    if idx:
        person = (
            Worker.select(Worker, Vacancy)
            .join_from(Worker, Vacancy)
            .where(Worker.id == idx)
        )
        tasks = (
            Task.select(
                Task, Status, peewee.fn.SUM(Period.value).alias('passed'))
            .join_from(Task, Status)
            .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
            .order_by(Task.status)
            .group_by(Task.id)
        )
        worker = peewee.prefetch(person, tasks).pop()
    else:
        worker = None
    return {
        'func_position': Vacancy.select(),
        'person': worker,
    }


def get_task_data(idx=None):
    print(f'{idx=}')
    return {
        'statuses': Status.select(),
        'workers': Worker.select(),
        'full_passed_of_order': (
            Task.select(Task, peewee.fn.SUM(Period.value).alias('passed'))
            .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
            .where(Task.order == Task[idx].order)
            .group_by(Task.order)),
        'task': (
            Task.select(Task, Status, Worker, peewee.fn.SUM(Period.value).alias('passed'))
            .join_from(Task, Status)
            .join_from(Task, Worker)
            .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
            .where(Task.id == idx)
            .group_by(Task.id)
        )
    }


def get_all_tasks():
    return (
        Task.select(
            Task.id, Task.type_obj, Task.title, Task.article, Task.order,
            Task.deadline, peewee.fn.SUM(Period.value).alias('total'),
            Status.state,
            Worker.surname, Worker.name, Worker.second_name, Worker.table_num,
            Vacancy.post.alias('post'), Vacancy.id
        )
        .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
        .join_from(Task, Status)
        .join_from(Task, Worker)
        .join_from(Worker, Vacancy)
    )


def get_close_tasks():
    return (
        get_all_tasks()
        .where(Status.state == sv[2])
        .group_by(Task.id)
    )


def get_mounter_tasks():
    return (
        get_all_tasks()
        .where(
            Status.state != sv[2],
            Worker.function.name.in_([fv[1], fv[2]])
        )
        .group_by(Task.id)
    )

    # @add_logger_peewee


def get_fitter_tasks():
    return (
        get_all_tasks()
        .where(
            Status.state != sv[2],
            Worker.function.name.in_([fv[3], fv[4]])
        )
        .group_by(Task.order)
    )
