from datetime import datetime

import peewee

from .models import (
    Worker, Vacancy, Task, Status, Period, Order, TypeTask, Month
)

now_date = datetime.now().date()


def get_subquery_worker(active=True):
    month = Month(now_date.month)
    start, mean, end = month.get_border_dates()

    return Worker.raw(
    "SELECT "
        "worker.id, worker.surname, worker.name, worker.second_name, "
        "worker.table_num, vacancy.post, typetask.title AS type_task, "
        "task.deadline AS dltask, 'order'.no AS order_num, sum(period.value) AS sum_period "
    "FROM worker "
    "JOIN vacancy ON worker.function_id = vacancy.id "
    "LEFT JOIN ("
        "SELECT *, row_number() OVER(PARTITION BY period.'worker_id' ORDER BY date DESC) AS rn "
        "FROM period "
        "JOIN task ON period.task_id = task.id "
        "JOIN status ON task.status_id = status.id "
        f"WHERE date >= '{now_date.year}-{now_date.month}-01' AND status.is_archived = 0 "
        f"AND date <= '{now_date.year}-{month.number}-{month.days}'"
    ") sub ON sub.'worker_id' = worker.id AND sub.rn = 1 "
    "LEFT JOIN period ON period.task_id = sub.task_id "
    "LEFT OUTER JOIN 'order' ON period.order_id = 'order'.id "
    "LEFT JOIN task ON period.task_id = task.id "
    "LEFT JOIN typetask ON task.is_type_id = typetask.id "
    f"WHERE worker.is_active = {active} "
    "GROUP BY worker.id "
    "ORDER BY worker.surname, worker.name, worker.second_name"
    )

    # sub = (
    #     Period.select(
    #         Period, peewee.fn.RANK().over(
    #             order_by=[Period.date.desc()],
    #             partition_by=[Period.worker_id],
    #         ).alias('rk'))
    #     .join(Task).join(Status)
    #     .where(~Status.is_archived, Period.date >= start, Period.date <= end)
    # )
    # return (
    #     Worker.select(
    #         Worker.id, Worker.surname, Worker.name, Worker.second_name, Worker.table_num,
    #         Vacancy.post,
    #         TypeTask.title.alias('type_task'),
    #         Task.deadline.alias('dltask'),
    #         Order.no.alias('order_num'),
    #         peewee.fn.SUM(Period.value).alias('sum_period'), Period.date)
    #     .join(Vacancy)
    #     .join(sub, peewee.JOIN.LEFT_OUTER, on=(sub.c.worker_id == Worker.id & sub.c.rk == 1))
    #     .join(Period, peewee.JOIN.LEFT_OUTER, on=(sub.c.task_id == Period.task_id))
    #     .join(Task, peewee.JOIN.LEFT_OUTER, on=(Period.task_id == Task.id))
    #     .join(TypeTask, on=(Task.is_type_id == TypeTask.id))
    #     .join(Order, peewee.JOIN.LEFT_OUTER, on=(Task.order_id == Order.id))
    #     # .where(sub.c.rk == 1)
    #     .group_by(Worker.id)
    #     .order_by(Worker.surname)
    #     .objects()
    # )


def get_workers_for_list():
    return Worker.select(Worker, Vacancy).join(Vacancy).where(Worker.is_active)


def get_all_workers():
    return get_subquery_worker()
    # return get_subquery_worker().where(Worker.is_active)


def get_all_dismiss():
    return get_subquery_worker(active=False)
    # return get_subquery_worker().where(~Worker.is_active)


def get_all_orders():
    orders = (
        Order.select(
            Order, peewee.fn.SUM(Period.value).alias('passed'),
            peewee.fn.MAX(Task.deadline).alias('deadline')
        )
        .join_from(Order, Period, peewee.JOIN.LEFT_OUTER)
        .join_from(Order, Task, peewee.JOIN.LEFT_OUTER)
        .where(
            Order.is_active,
            Order.id.not_in(Task.select(Task.order)) |
            Order.id.in_(Task.select(Task.order).join_from(Task, Status).where(~Status.is_archived))
        )
        .group_by(Order.id)
    )

    tasks = Task.select(Task, Status).join(Status).where(Task.is_active, ~Status.is_archived)

    return peewee.prefetch(orders, tasks)


def get_worker_data(idx=None):
    print(f'{idx=}')
    if idx:
        person = (
            Worker.select(Worker, Vacancy)
            .join_from(Worker, Vacancy)
            .where(Worker.id == idx).get()
        )
        tasks = (
            Task.select(
                Task, Status, Worker, Order, Period,
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
    query = {
        'statuses': Status.select(),
        'types': TypeTask.select()
    }
    if idx:
        task = (
            Task.select(Task, Status, Worker, Order, TypeTask)
            .join_from(Task, Status)
            .join_from(Task, Order, peewee.JOIN.LEFT_OUTER)
            .join_from(Task, Worker)
            .join_from(Task, TypeTask)
            .where(Task.id == idx)
            .get()
        )
        periods = Period.select(Period, Worker, Vacancy).join(Worker).join(Vacancy).order_by(Period.date)
        order = task.order
        passed_order = periods.where(Period.order == order)
        query['task'] = task

        query['passed_task'] = sum(periods.where(Period.task == task))
        query['passed_order'] = sum(passed_order if order else [])
        query['passed_mont'] = sum(passed_order.where(Vacancy.is_mounter) if order else [])
        query['passed_fitter'] = sum(passed_order.where(Vacancy.is_fitter) if order else [])
        query['time_worked'] = periods.where(Period.task == task)
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
        Task.select(
            Task, Order, Status, Period, Worker,
            TypeTask, peewee.fn.SUM(Period.value).alias('passed'))
        .join_from(Task, Status)
        .join_from(Task, Worker)
        .join_from(Task, TypeTask)
        .join_from(Task, Order, peewee.JOIN.LEFT_OUTER)
        .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
        .group_by(Task.id)
    )


def get_close_tasks():
    return (
        get_all_tasks()
        .where(
            Task.is_active, Status.is_archived,
            Period.date.year == now_date.year,
            Period.date.month == now_date.month
        )
    )


def get_open_tasks():
    return (
        get_all_tasks()
        .where(Task.is_active, ~Status.is_archived)
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


def delete_or_restore(key, idx):
    models = {'worker': Worker, 'task': Task, 'order': Order}
    model = models.get(key)
    if key == 'worker':
        return model.update(is_active=~model.is_active).where(model.id == idx).execute()
    else:
        return model.get(model.id == idx).delete_instance(recursive=True)



def get_period(idx=None):
    if idx:
        return Period[idx]
    return None


def update_delete_period(data, action):
    print(f'update_delete_period {data=}')
    idx = int(data.pop('period_id'))
    if action == '-SAVE-PER-':
        if data:
            return Period.update(**data).where(Period.id == idx).execute()
        return None
    elif action == '-DEL-PER-':
        return Period.delete().where(Period.id == idx).execute()


def get_query_for_exel(worker, month):
    current_periods = (
        Period.select(Period, Task).join(Task)
        .where(Period.date.year == now_date.year, Period.date.month == month.number)
        .order_by(Period.date)
    )
    prev_periods = (
        Period.select(Period, Task).join(Task)
        .where(Period.date.year == now_date.year, Period.date.month < month.number)
        .order_by(Period.date)
    )

    worker_periods = (
        Period.select(Period, Worker).join(Worker)
        .where(Period.worker == worker, Period.date.year == now_date.year, Period.date.month == month.number)
        .order_by(Period.date)
    )

    sub = Period.select(Period.task).where(Period.date.year == now_date.year, Period.date.month == month.number)

    tasks = (
        Task.select(Task, Order, Status, Worker, TypeTask)
        .join_from(Task, Order)
        .join_from(Task, Status)
        .join_from(Task, Worker)
        .join_from(Task, TypeTask)
        .where(Task.worker == worker, Task.id.in_(sub))
    )

    prev = Task.select().join(Worker).where(Task.worker == worker, Task.id.in_(sub))

    return {
        'current_task': peewee.prefetch(tasks, current_periods),
        'prev_task': peewee.prefetch(prev, prev_periods),
        'first_half': worker_periods.where(Period.date.day <= month.get_means()),
        'second_half': worker_periods.where(Period.date.day > month.get_means()),
    }


def get_query_for_timesheet(month):
    month = Month(month)
    start, mean, end = month.get_border_dates()
    w = Worker.select(Worker, Vacancy).join(Vacancy).order_by(Worker.surname, Worker.name, Worker.second_name)
    p = (
        Period.select(
            Period, peewee.fn.SUM(Period.value).over(partition_by=[Period.worker, Period.date]).alias('sum_val'))
        .where(Period.date >= start, Period.date <= end).order_by(Period.date))
    return peewee.prefetch(w, p)
