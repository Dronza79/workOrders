from database.queries import get_query_for_exel


def get_personal_table_result(worker, month):
    query = get_query_for_exel(worker, month)
    current_task = query['current_task']
    prev_task = query['prev_task']

    # for i, task in enumerate(current_task):
    #     print(f'{f" до:{sum(prev_task[i].time_worked)} ч.=={task}=={sum(task.time_worked)} ч.":=^50}')
    #     for period in task.time_worked:
    #         print(f'{period}')

    for idx in range(0, len(current_task) + 1, 6):
        print(f'{current_task[0 + idx:6 + idx]=}')
