from datetime import datetime

import peewee

from .models import (
    Worker, Vacancy, Task, Status, Period, Order, TypeTask,
)

now_date = datetime.now().date()


def get_subquery_worker():
    return (
        Period.select(Period, Task, Order, Worker, Status)
        .join_from(Period, Task).join_from(Period, Order, peewee.JOIN.LEFT_OUTER)
        .join_from(Period, Worker).join_from(Task, Status)
        .where(
            ~Status.is_archived,
            Period.date.year == now_date.year,
            Period.date.month == now_date.month
        )
        .order_by(Period.date)
    ), (
        Task.select(Task, Worker, Order, Status, Period, peewee.fn.SUM(Period.value).alias('total_time'))
        .join_from(Task, Period, peewee.JOIN.LEFT_OUTER).join_from(Task, Order, peewee.JOIN.LEFT_OUTER)
        .join_from(Task, Worker).join_from(Task, Status)
        .where(
            ~Status.is_archived,
            Period.date.year == now_date.year,
            Period.date.month == now_date.month
        )
        .order_by(Period.date)
        .group_by(Task.id)
    )


def get_all_workers():
    persons = (
        Worker
        .select(Worker.id, Worker.table_num, Worker.surname, Worker.name, Worker.second_name, Vacancy.post)
        .join(Vacancy).where(Worker.is_active)
    )

    periods, tasks = get_subquery_worker()
    return peewee.prefetch(persons, periods, tasks)


def get_all_dismiss():
    persons = (
        Worker
        .select(Worker.id, Worker.table_num, Worker.surname, Worker.name, Worker.second_name, Vacancy.post)
        .join(Vacancy).where(~Worker.is_active)
    )

    periods, tasks = get_subquery_worker()
    return peewee.prefetch(persons, periods, tasks)


def get_all_orders():
    orders = (
        Order.select(
            Order, peewee.fn.SUM(Period.value).alias('passed'),
            peewee.fn.MAX(Task.deadline).alias('deadline')
        )
        .join_from(Order, Period, peewee.JOIN.LEFT_OUTER)
        .join_from(Order, Task, peewee.JOIN.LEFT_OUTER)
        .where(
            Order.id.not_in(Task.select(Task.order)) |
            Order.id.in_(Task.select(Task.order).join_from(Task, Status).where(~Status.is_archived))
        )
        .group_by(Order.id)
    )

    tasks = Task.select().join(Status).where(Task.is_active, ~Status.is_archived)


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
                Status, Worker, Order, Period,
                peewee.fn.SUM(Period.value).alias('passed'),
            )
            .join_from(Task, Status)
            .join_from(Task, Worker)
            .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
            .join_from(Task, Order, peewee.JOIN.LEFT_OUTER)
            .where(Worker.id == idx, ~Status.is_archived)
            .group_by(Task.id)
            .order_by(-Status.is_positive, -peewee.fn.MAX(Period.date))
        )
    else:
        person = None
        tasks = None
    return {
        'func_position': Vacancy.select(),
        'worker': person,
        'tasks': tasks
    }


def get_task_data(idx=None):
    # print(f'get_task_data {idx=}')
    query = {
        'statuses': Status.select(),
        'types': TypeTask.select()
    }
    if idx:
        query['task'] = (
            Task.select(Task, Status, Worker, Order, TypeTask)
            .join_from(Task, Status)
            .join_from(Task, Order, peewee.JOIN.LEFT_OUTER)
            .join_from(Task, Worker)
            .join_from(Task, TypeTask)
            .where(Task.id == idx)
            # .group_by(Task.id)
            .get()
        )
        periods = Period.select().where(Period.task_id == idx)

        query['passed_task'] = sum(query['task'].time_worked)
        query['passed_order'] = sum(query['task'].order.time_worked if query['task'].order else [])
        # query['time_worked'] = periods.where(Period.date.year == now_date.year, Period.date.month == now_date.month)
        query['time_worked'] = periods
    else:
        query['workers'] = Worker.select(Worker, Vacancy.post).join(Vacancy)
        query['all_orders'] = (
            Order.select(Order, peewee.fn.SUM(Period.value).alias('passed'))
            .join_from(Order, Period, peewee.JOIN.LEFT_OUTER)
            .where(
                Order.id.not_in(Task.select(Task.order)) |
                Order.id.in_(Task.select(Task.order).join(Status).where(~Status.is_archived))
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
                .join_from(Task, Order, peewee.JOIN.LEFT_OUTER)
                .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
                .where(Task.order_id == idx)
                .group_by(Task.id)
            )
        }
    else:
        return None


def get_all_tasks():
    return (
        Task.select(Task, Order, Status, Period, Worker, TypeTask, peewee.fn.SUM(Period.value).alias('passed'))
        .join_from(Task, Status)
        .join_from(Task, Worker)
        .join_from(Task, TypeTask)
        .join_from(Task, Order, peewee.JOIN.LEFT_OUTER)
        .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
    )


def get_close_tasks():
    return (
        get_all_tasks()
        .where(Task.is_active, Status.is_archived)
        .group_by(Task.id)
    )


def get_open_tasks():
    return (
        get_all_tasks()
        .where(Task.is_active, ~Status.is_archived)
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

# import datetime
# import peewee
# from database.models import Worker, Task, Period, Order, Vacancy, Status
# def get_query_for_exel():
#     # import logging
#     # logger = logging.getLogger('peewee')
#     # logger.addHandler(logging.StreamHandler())
#     # logger.setLevel(logging.DEBUG)
#
#     date_from = datetime.datetime(2024, 8, 3).date()
#     date_to = datetime.datetime(2024, 8, 14).date()
#
#     worker = Worker.select(Worker, Vacancy.post).join(Vacancy).get()
#     periods = Period.select(Period, Task).join(Task).where(Period.date >= date_from, Period.date <= date_to)
#     sub = Period.select(Period.task).where(Period.date >= date_from, Period.date <= date_to)
#     before = Period.select(Period, Task).join(Task).where(Period.date < date_from)
#     tasks = (
#             Task.select(Task, Order, Status, peewee.fn.SUM(Period.value).alias('passed'))
#             .join_from(Task, Order)
#             .join_from(Task, Status)
#             .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
#             .where(Task.worker == worker, Task.id.in_(sub))
#             .group_by(Task.id)
#         )
#     bef_task = Task.select().where(Task.id.in_(Task.select(Task.id).where(Task.worker == worker, Task.id.in_(sub))))
#
#     return {
#         'worker': worker,
#         'task': peewee.prefetch(tasks, periods),
#         'before': peewee.prefetch(bef_task, before)
#     }
# query = get_query_for_exel()
# for i, task in enumerate(query['task']):
#     print(f'{"="*10}{sum(query["before"][i].time_worked)=}::{task}::{sum(task.time_worked)}{"="*10}')
#     # print(f'{"="*10}{task.passed=}::{task}::{sum(task.time_worked)}{"="*10}')
#     for per in task.time_worked:
#         print(f'{per}')
