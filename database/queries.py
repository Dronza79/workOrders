import datetime

import peewee

from .models import (
    Worker, Vacancy, Task, Status, Period, Order,
    STATUS_VARIABLES as sv,
    FUNC_VARIABLES as fv,
)


def get_subquery_worker():
    return (
        Period.select(Period, Task, Order, Worker)
        .join_from(Period, Task).join_from(Period, Order)
        .join_from(Period, Worker).where(Task.status_id != 3)
        .order_by(Period.date).group_by(Period.id)
    ), (
        Task.select(Task, Worker, Order, Status, peewee.fn.SUM(Period.value).alias('total_time'))
        .join_from(Task, Period, peewee.JOIN.LEFT_OUTER).join_from(Task, Order)
        .join_from(Task, Worker).join_from(Task, Status)
        .order_by(Period.date).group_by(Task.id)
    )


def get_all_workers():
    persons = (
        Worker
        .select(Worker.id, Worker.table_num, Worker.surname, Worker.name, Worker.second_name, Vacancy.post)
        .join(Vacancy).where(Worker.is_active == True)
    )

    periods, tasks = get_subquery_worker()
    return peewee.prefetch(persons, periods, tasks)


def get_all_dismiss():
    persons = (
        Worker
        .select(Worker.id, Worker.table_num, Worker.surname, Worker.name, Worker.second_name, Vacancy.post)
        .join(Vacancy).where(Worker.is_active == False)
    )

    periods, tasks = get_subquery_worker()
    return peewee.prefetch(persons, periods, tasks)


def get_all_orders():
    orders = (
        Order.select()
        .where(
            Order.id.not_in(Task.select(Task.order)) |
            Order.id.in_(Task.select(Task.order).join(Status).where(Task.status.state.in_([sv[1], sv[2]])))
        )
        .group_by(Order.id)
    )

    tasks = (
        Task.select(Task, Worker.surname, Worker.name, Worker.second_name)
        .join_from(Task, Worker)
        .group_by(Task.id)
    )

    return peewee.prefetch(orders, tasks)


def get_worker_data(idx=None):
    # print(f'{idx=}')
    if idx:
        person = (
            Worker.select(Worker, Vacancy)
            .join_from(Worker, Vacancy)
            .where(Worker.id == idx).get()
        )
        tasks = (
            Task.select(
                Task.id, Task.deadline, Task.comment,
                Status, Worker, Order,
                peewee.fn.SUM(Period.value).alias('passed'))
            .join_from(Task, Status)
            .join_from(Task, Worker)
            .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
            .join_from(Task, Order)
            .where(Worker.id == idx)
            .order_by(Task.status)
            .group_by(Task.id)
        )
        # query = peewee.prefetch(person, tasks).pop()
    else:
        person = None
        tasks = None
    return {
        'func_position': Vacancy.select(),
        'worker': person,
        'tasks': tasks
    }


def get_task_data(idx=None):
    print(f'get_task_data {idx=}')
    query = {'statuses': Status.select()}
    if idx:
        query['task'] = (
            Task.select(Task, Status, Worker, Order)
            .join_from(Task, Status)
            .join_from(Task, Order)
            .join_from(Task, Worker)
            .where(Task.id == idx)
            .group_by(Task.id)
            .get()
        )
        periods = Period.select().where(Period.task_id == idx)
        query['passed'] = sum(periods)
        query['time_worked'] = periods
    else:
        query['workers'] = Worker.select(Worker, Vacancy.post).join(Vacancy)
        query['all_orders'] = (
            Order.select(Order, peewee.fn.SUM(Period.value).alias('passed'))
            .join_from(Order, Period, peewee.JOIN.LEFT_OUTER)
            .where(
                Order.no.not_in(Task.select(Task.order)) |
                Order.no.in_(Task.select(Task.order).join(Status).where(Task.status.state.in_([sv[1], sv[2]])))
            )
            .group_by(Order.id)
        )

    return query


def get_order_data(idx=None):
    if idx:
        return {
            'order': Order.select().where(Order.id == idx).get(),
            'tasks': (
                Task.select(
                    Task, Status, Worker, Order,
                    peewee.fn.SUM(Period.value).alias('passed')
                )
                .join_from(Task, Status)
                .join_from(Task, Worker)
                .join_from(Task, Order)
                .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
                .where(Task.order_id == idx)
                .group_by(Task.id)
            )
        }
    else:
        return None


def get_all_tasks():
    return (
        Task.select(
            Task.id, Task.deadline, peewee.fn.SUM(Period.value).alias('total_worked'),
            Order.no,
            Status.state,
            Period.value,
            Worker.surname, Worker.name, Worker.second_name
        )
        .join_from(Task, Status)
        .join_from(Task, Worker)
        .join_from(Task, Order)
        .join_from(Order, Period, peewee.JOIN.LEFT_OUTER)
    )


def get_close_tasks():
    return (
        get_all_tasks()
        .where(Status.state == sv[2])
        .group_by(Task.id)
    )


def get_open_tasks():
    return (
        get_all_tasks()
        .where(Status.state != sv[3])
        .group_by(Task.id)
    )


def create_new_period(data):
    return Period.create(**data)


def create_or_update_entity(key, data, idx):
    model = Worker if key == 'worker' else Order if key == 'order' else Task
    if idx:
        result = model.update(**data).where(model.id == idx).execute()
    else:
        result = model.create(**data)

    return result


def delete_or_restore_worker(idx):
    return Worker.update(is_active=~Worker.is_active).where(Worker.id == idx).execute()


def get_period(pos, task):
    task = Task.select().join(Period, peewee.JOIN.LEFT_OUTER).where(Task.id == int(task)).get()
    return task.time_worked[pos]


def update_delete_period(data, action):
    print(f'update_delete_period {data=}')
    idx = int(data.pop('period_id'))
    if action == '-SAVE-PER-':
        if data:
            return Period.update(**data).where(Period.id == idx).execute()
        return None
    elif action == '-DEL-PER-':
        return Period.delete().where(Period.id == idx).execute()


import datetime
import peewee
from database.models import Worker, Task, Period, Order, Vacancy, Status
from database.app_logger import add_logger_peewee
@add_logger_peewee
def get_query_for_exel():
    worker = Worker[1]
    query = {}
    date_from = datetime.datetime(2024, 8, 1).date()
    date_to = datetime.datetime(2024, 8, 11).date()

    return (
        Worker.select(Worker, Task, Status, Period, Vacancy)
        .join_from(Worker, Vacancy)
        .join_from(Worker, Task, peewee.JOIN.LEFT_OUTER)
        .join_from(Task, Status)
        .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
        .where((Worker.id == worker.id) & (Period.date >= date_from) & (Period.date <= date_to)))
