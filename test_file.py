from datetime import datetime

import peewee
from peewee import fn

from database.app_logger import add_logger_peewee
from database.models import Worker, Task, TypeTask, Period, Status, Vacancy, Order
from database.settings import get_database


@add_logger_peewee
def main():
    current_date = datetime.now().date()
    raw_query = Worker.raw(
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
            f"WHERE date >= '{current_date.year}-{current_date.month}-01' AND status.is_archived = 0"
        ") sub ON sub.'worker_id' = worker.id AND sub.rn = 1 "
        "LEFT JOIN period ON period.task_id = sub.task_id "
        "LEFT OUTER JOIN 'order' ON period.order_id = 'order'.id "
        "LEFT JOIN task ON period.task_id = task.id "
        "LEFT JOIN typetask ON task.is_type_id = typetask.id "
        "WHERE worker.is_active = 1 "
        "GROUP BY worker.id "
        "ORDER BY worker.surname, worker.name, worker.second_name"
    )

    dash = '--'
    # Вывод результатов
    for i, worker in enumerate(raw_query, start=1):
        print(i, end='\t')
        print(f'{f"{worker.surname} {worker.name} {worker.second_name}":<35}', end='\t')
        print(worker.table_num, end='\t')
        print(f'{worker.post:<18}', end='\t')
        print(f"{worker.type_task if worker.type_task else dash:<10}", end='\t')
        print(f"{f'ПР-{worker.order_num:06}' if worker.order_num else dash:<9}", end='\t')
        print(worker.dltask if worker.dltask else dash, end='\t')
        print(worker.sum_period if worker.sum_period else dash, end='\t')
        print(worker.id, end='\t')
        print()


# select worker.surname, worker.name, worker.second_name, worker.table_num, vacancy.post, typetask.title, task.deadline, 'order'.no, sum(period.value) as sum_value
# from (
# select *,
#        row_number() over(partition by worker_id order by date desc) as rn
# from period
# where date >= '2024-10-01'
# ) sub
# join period on period.task_id = sub.task_id
# join worker on period.worker_id = worker.id
# join vacancy on worker.function_id = vacancy.id
# left outer join 'order' on period.order_id = 'order'.id
# join task on period.task_id = task.id
# join typetask on task.is_type_id = typetask.id
# where rn = 1
# group by sub.worker_id, sub.task_id
# order by worker.surname, worker.name, worker.second_name
# ;

if __name__ == '__main__':
    main()
