from .models import *

now_date = dd.now()


def get_subquery_worker(active=True):
    sub_query = (
        Period.select(
            Period, Task,
            fn.row_number().over(partition_by=[Period.worker], order_by=[Period.date.desc()]).alias('rn'))
        .join(Task, on=(Period.task == Task.id))
        .join(Status, on=(Task.status == Status.id))
        .where(~Status.is_archived)
        .cte('sub'))

    return (
        Worker.select(
            Worker.id, Worker.surname, Worker.name, Worker.second_name, Worker.ordinal,
            Worker.table_num, Vacancy.post, TypeTask.title.alias('type_task'), Task.deadline.alias('dltask'),
            Order.no.alias('order_num'), fn.SUM(Period.value).alias('sum_period'))
        .join(Vacancy, on=(Worker.function == Vacancy.id))
        .join(sub_query, JOIN.LEFT_OUTER, on=((sub_query.c.worker_id == Worker.id) & (sub_query.c.rn == 1)))
        .join(Period, JOIN.LEFT_OUTER, on=(Period.task == sub_query.c.task_id))
        .join(Order, JOIN.LEFT_OUTER, on=(Period.order == Order.id))
        .join(Task, JOIN.LEFT_OUTER, on=(Period.task == Task.id))
        .join(TypeTask, JOIN.LEFT_OUTER, on=(Task.is_type == TypeTask.id))
        .where(Worker.is_active == active)
        .group_by(Worker.id)
        .order_by(Worker.ordinal, Worker.surname, Worker.name, Worker.second_name)
        .with_cte(sub_query)
        .dicts()
    )


def get_workers_for_list():
    return Worker.select(Worker, Vacancy).join(Vacancy).where(Worker.is_active).order_by(Worker.ordinal)


def get_all_workers():
    return get_subquery_worker()


def get_all_dismiss():
    return get_subquery_worker(active=False)


def get_all_orders():
    orders = (
        Order.select(
            Order, fn.SUM(Period.value).alias('passed'),
            fn.MAX(Task.deadline).alias('deadline')
        )
        .join_from(Order, Period, JOIN.LEFT_OUTER)
        .join_from(Order, Task, JOIN.LEFT_OUTER)
        .where(
            Order.is_active,
            Order.id.not_in(Task.select(Task.order)) |
            Order.id.in_(Task.select(Task.order).join_from(Task, Status).where(~Status.is_archived))
        )
        .group_by(Order.id)
    )

    tasks = Task.select(Task, Status).join(Status).where(Task.is_active, ~Status.is_archived)

    return prefetch(orders, tasks)


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
                fn.SUM(Period.value).alias('passed'),
            )
            .join_from(Task, Status)
            .join_from(Task, Worker)
            .join_from(Task, Period, JOIN.LEFT_OUTER)
            .join_from(Task, Order, JOIN.LEFT_OUTER)
            .where(Worker.id == idx)
            .group_by(Task.id)
            .order_by(Status.is_archived, -Status.is_positive, -fn.MAX(Period.date))
        )
    else:
        person = None
        tasks = None
    return {
        'func_position': Vacancy.select().where(Vacancy.is_active),
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
            .join_from(Task, Order, JOIN.LEFT_OUTER)
            .join_from(Task, Worker)
            .join_from(Task, TypeTask)
            .where(Task.id == idx)
            .get()
        )
        periods = Period.select(Period, Worker, Vacancy).join(Worker).join(Vacancy).order_by(Period.date)
        order = task.order
        passed_order = periods.where(Period.order == order)
        query['task'] = task

        query['passed_task'] = sum(periods.where(Period.task == task).iterator())
        query['passed_order'] = sum(passed_order if order else [])
        query['passed_mont'] = sum(passed_order.where(Vacancy.is_mounter) if order else [])
        query['passed_fitter'] = sum(passed_order.where(Vacancy.is_fitter) if order else [])
        query['time_worked'] = periods.where(Period.task == task).iterator()
    else:
        query['workers'] = Worker.select(Worker, Vacancy.post).join(Vacancy).where(Worker.is_active)
        query['all_orders'] = (
            Order.select(Order, fn.SUM(Period.value).alias('passed'))
            .join_from(Order, Period, JOIN.LEFT_OUTER)
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
                    fn.SUM(Period.value).alias('passed')
                )
                .join_from(Task, Status)
                .join_from(Task, Worker)
                .join_from(Task, Order, JOIN.LEFT_OUTER)
                .join_from(Task, Period, JOIN.LEFT_OUTER)
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
            TypeTask, fn.SUM(Period.value).alias('passed'),
            fn.MAX(Period.date).alias('max_date')
        )
        .join_from(Task, Status)
        .join_from(Task, Worker)
        .join_from(Task, TypeTask)
        .join_from(Task, Order, JOIN.LEFT_OUTER)
        .join_from(Task, Period, JOIN.LEFT_OUTER)
        .group_by(Task.id)
    )


def get_close_tasks():
    return (
        get_all_tasks()
        .where(
            Task.is_active, Status.is_archived,
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
        return Period.get_by_id(idx)
    return None


def update_delete_period(data, action):
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
        .where(Period.date.year == month.year, Period.date.month == month.number)
        .order_by(Period.date)
    )
    prev_periods = (
        Period.select(Period, Task).join(Task)
        .where(Period.date.year == month.year, Period.date.month < month.number)
        .order_by(Period.date)
    )

    worker_periods = (
        Period.select(Period, Worker).join(Worker)
        .where(Period.worker == worker, Period.date.year == month.year, Period.date.month == month.number)
        .order_by(Period.date)
    )

    sub = Period.select(Period.task).where(Period.date.year == month.year, Period.date.month == month.number)

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
        'current_task': prefetch(tasks, current_periods),
        'prev_task': prefetch(prev, prev_periods),
        'first_half': worker_periods.where(Period.date.day <= month.get_means()),
        'second_half': worker_periods.where(Period.date.day > month.get_means()),
    }


def get_query_for_timesheet(month: Month):
    start, end = month.get_between()
    w = Worker.select(Worker, Vacancy).join(Vacancy).order_by(Worker.surname, Worker.name, Worker.second_name)
    p = (
        Period.select(
            Period, fn.SUM(Period.value).over(partition_by=[Period.worker, Period.date]).alias('sum_val'))
        .where(Period.date >= start, Period.date <= end).order_by(Period.date))
    return prefetch(w, p)


def get_list_years():
    return [year for year in range(
        Period.select().order_by(Period.date).limit(1).get().date.year,
        now_date.year + 1
    )]


def get_query_kpi(month: Month):
    st, ed = month.get_between()

    P1 = Period.alias()
    P2 = Period.alias()
    P3 = Period.alias()

    sum_current = (P1.select(fn.SUM(P1.value))
                   .where((P1.task == Task.id) & (P1.date.between(st, ed))))
    sum_before = (P2.select(fn.SUM(P2.value))
                  .where((P2.task == Task.id) & (P2.date < st)))
    has_future = (P3.select(fn.COUNT(P3.id))
                  .where((P3.task == Task.id) & (P3.date > ed)))

    part_deadline = Task.deadline.cast('REAL') * .3

    task_kpi = Case(None, [
        ((has_future > 0) | (Status.state != 'Завершен'), fn.COALESCE(sum_current, 0)),
        # ((Status.state == 'Завершен') & (fn.COALESCE(sum_current, 0) * 5 < Task.deadline), fn.COALESCE(sum_current, 0)),
        (fn.COALESCE(sum_current, 0) <= part_deadline, fn.COALESCE(sum_current, 0)),
    ], (Task.deadline - fn.COALESCE(sum_before, 0)))

    task_subquery = (
        Task.select(
            Task.worker.alias('worker_id'),
            task_kpi.alias('kpi_val'),
            fn.COALESCE(sum_current, 0).alias('hours_val')
        )
        .join(Status)
        .where(Task.id << Period.select(Period.task).where(Period.date.between(st, ed)))
        .alias('task_sub'))

    query = (
        Worker.select(
            Worker,
            fn.COALESCE(fn.SUM(task_subquery.c.kpi_val), 0).alias('total_plan'),
            fn.COALESCE(fn.SUM(task_subquery.c.hours_val), 0).alias('total_fact')
        )
        .join(task_subquery, JOIN.LEFT_OUTER, on=(Worker.id == task_subquery.c.worker_id))
        .where(Worker.is_active)
        .group_by(Worker.id)
        .order_by(Worker.ordinal)
    )

    return query


def get_query_reg():
    return {
        'vacancy': {
            'query': Vacancy.select(
                Vacancy.id, Vacancy.post, Vacancy.is_slave,
                Vacancy.is_staff, Vacancy.is_mounter,
                Vacancy.is_fitter, Vacancy.is_checked, Vacancy.is_store
            ).where(Vacancy.is_active),
            'name_field': ['post', 'Должность'],
            'check_field': [
                ['is_slave', 'Подчиненый'],
                ['is_mounter', 'Монтажник'],
                ['is_checked', 'Приемка'],
                ['is_staff', 'Персонал'],
                ['is_fitter', 'Сборщик'],
                ['is_store', 'Склад']
            ],
            'idx': 'vac_id',
            'listbox': 'VAC',
        },
        'status': {
            'query': Status.select(
                Status.id, Status.state, Status.is_positive,
                Status.is_archived).where(Status.is_active),
            'name_field': ['state', 'Состояние'],
            'check_field': [
                ['is_positive', 'Позитивно'],
                ['is_archived', 'Завершено']
            ],
            'idx': 'status_id',
            'listbox': 'STATUS',
        },
        'type_task': {
            'query': TypeTask.select(
                TypeTask.id, TypeTask.title, TypeTask.has_extension).where(TypeTask.is_active),
            'name_field': ['title', 'Тип работы'],
            'check_field': [
                ['has_extension', 'Предусмотрена ПРка']
            ],
            'idx': 'type_id',
            'listbox': 'TYPE',
        }
    }


def request_post_reg_data(model, model_id, delete=False, **valid_data):
    print(f'{valid_data=}\n{model=}\n{delete=}')
    if not model_id:
        model.create(**valid_data)
    elif delete:
        model.update(is_active=False).where(model.id == model_id).execute()
    else:
        model.update(**valid_data).where(model.id == model_id).execute()
    return model.select().where(model.is_active)


def get_query_sys():
    return ProgramSetting.select(
        ProgramSetting.major, ProgramSetting.minor, ProgramSetting.patch,
        ProgramSetting.org, ProgramSetting.div, ProgramSetting.resp_post, ProgramSetting.resp_name,
        ProgramSetting.head_post, ProgramSetting.head_name, ProgramSetting.m_theme).get()


def req_post_program_setting(valid):
    sett = ProgramSetting.get_setting()
    for key in valid:
        setattr(sett, key, valid[key])
    print(f'{sett.save()=}')
