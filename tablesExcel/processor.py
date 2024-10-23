import PySimpleGUI as sg

from database.queries import get_query_for_exel
from gui.templates_settings import output_setting
from tablesExcel.forms import PersonalMonthExelTable


def get_personal_table_result(worker, month):
    query = get_query_for_exel(worker, month)
    current_task = query.pop('current_task')
    prev_task = query.pop('prev_task')
    len_pages = len(current_task) // 6 + (1 if len(current_task) % 6 else 0)
    exel = PersonalMonthExelTable()
    target = sum(map(lambda x: x.deadline, current_task)) - sum(map(lambda x: sum(x.time_worked), prev_task))

    for idx in range(0, len(current_task) + 1, 6):
        cur_page = current_task[0 + idx:6 + idx]
        prev_data = prev_task[0 + idx:6 + idx]
        exel.fill_data(worker, month, query, target, cur_page, prev_data)
        len_pages -= 1
        if len_pages:
            exel.add_worksheet()

    return exel.save(f'{worker.surname}_{month.number:02}')


# for i, task in enumerate(current_task):
    # string = f'{f" до:{sum(prev_task[i].time_worked)} ч.=={task}=={sum(task.time_worked)} ч.":=^50}'
    # sg.Print(string, **output_setting)
    # for period in task.time_worked:
    #     sg.Print(f'{period}', **output_setting)

