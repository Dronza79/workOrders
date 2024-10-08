import PySimpleGUI as sg

from .templates_settings import table_setting, input_setting, drop_down_setting, text_setting, multiline_setting, \
    delete_button_setting, table_period_setting, frame_setting, table_tasks_setting


def get_sector_workers(code=''):
    heads = ['№ п/п', 'Фамилия имя отчество', 'Таб.номер', 'Должность', 'Номер ПР', 'Норматив', 'Отработано']
    width_cols = [4, 30, 10, 16, 10, 7, 7]
    return [[
        sg.Table(
            values=[],
            headings=heads,
            key=code,
            col_widths=width_cols,
            **table_setting)
    ]]


def get_sector_orders():
    heads = [
        '№', 'Номер ПР', 'Тип', 'Объект', "Конструктив", 'Работник']
    width_cols = [3, 10, 12, 12, 22, 11]
    return [[
        sg.Table(
            values=[], headings=heads, key='-ORDERS-',
            col_widths=width_cols,
            **table_setting)
    ]]


def get_sector_tasks(code=''):
    heads = [
        '№', 'Номер ПР', 'Норма', 'Вып.', "Работник", 'Статус']
    width_cols = [3, 10, 5, 5, 13, 8]
    return [[
        sg.Table(
            values=[], headings=heads, key=code,
            col_widths=width_cols,
            **table_setting)
    ]]


def get_list_task_for_worker(query):
    return [
        [
            i, task.status, task.order.title, task.order.article,
            task.order, task.deadline, task.passed, task.comment, task.id
        ] for i, task in enumerate(query, start=1)
    ]


def get_list_task_for_order(query):
    return [
        [
            i, task.status, task.deadline, task.passed, task.worker, task.comment
        ] for i, task in enumerate(query, start=1)
    ]


def get_card_worker(data):
    job_list = list(data['func_position'])
    worker = data.get('worker')
    tasks = data.get('tasks')
    table_heads = ['№', 'Статус', 'Объект', 'Артикул', 'ПРка', 'Норма', 'Вып.', 'Коммент']
    width_cols = [3, 8, 12, 20, 10, 5, 5, 14]
    if worker:
        buttons = ([[
            sg.Button(
                'Исключить',
                key='-DELETE-',
                disabled=False if worker.is_active else True,
                **delete_button_setting
            ),
            sg.Button(
                'Вернуть',
                key='-RESTORE-',
                disabled=True if worker.is_active else False,
                **delete_button_setting
            )
        ]])
        table = [[
            sg.Frame('Связанные задачи:', [
                [sg.Input(worker.id, key='worker_id', visible=False)],
                [sg.Table(
                    get_list_task_for_worker(tasks),
                    table_heads,
                    col_widths=width_cols,
                    num_rows=3,
                    key='-DOUBLE-TASKS-',
                    **table_tasks_setting)]
            ], size=(330, 150), **frame_setting)
        ]]
    else:
        buttons = []
        table = []

    return [sg.pin(sg.Col([[
        sg.Frame('Персональные данные:', [[sg.Col([
            [
                sg.Input('worker', key='type', visible=False),
                sg.T("Фамилия:", **text_setting),
                sg.Push(),
                sg.Input(worker.surname.upper() if worker else '', key='surname', **input_setting)
            ], [
                sg.Text("Имя:", **text_setting),
                sg.Push(),
                sg.Input(worker.name if worker else '', key='name', **input_setting)
            ], [
                sg.T("Отчество:", **text_setting),
                sg.Push(),
                sg.Input(worker.second_name if worker else '', key='second_name', **input_setting)
            ],
        ], pad=15, vertical_alignment='center')]], **frame_setting)], [
        sg.Frame('Служебные данные:', [[sg.Col([
            [
                sg.T('Табельный номер:', **text_setting),
                sg.Push(),
                sg.Input(worker.table_num if worker else '', key='table_num',
                         **input_setting)
            ], [
                sg.T('Должность:', **text_setting),
                sg.Push(),
                sg.Combo(
                    job_list,
                    key='function',
                    default_value=worker.function if worker else 'Не выбрано',
                    **drop_down_setting)
            ]] + buttons, pad=10)]], **frame_setting)],
        *table
    ], pad=0))]


def get_card_task(data):
    # print(f'get_card_task {data=}')
    time_worked = [
        [f'{period.date:%d.%m.%y}',
         f'{period.date:%a}',
         f'{period.value} ч.',
         ] for period in data.get('time_worked', [])]
    headers = ['Дата', 'Дн.нед.', 'Время']
    width_cols = [10, 5, 5]
    if task := data.get('task'):
        table = [[
            sg.Frame('Табель времени:', [
                [sg.Input(task.id, key='task', visible=False)],
                [
                    sg.Table(
                        time_worked,
                        headings=headers,
                        col_widths=width_cols,
                        key='-TIME-WORKED-',
                        **table_period_setting),
                    sg.Button(
                        'Добавить\nвремя',
                        key='-ADD-TIME-',
                        size=(10, 3), pad=10)
                ]
            ], size=(330, 150), **frame_setting)
        ]]
    else:
        table = []
    statuses = list(data.get('statuses', []))
    workers = list(data.get('workers', []))
    all_order = list(data.get('all_orders', []))

    return [sg.pin(sg.Col([[
        sg.Frame('Заказ:', [[sg.Col([[
            sg.Input('task', key='type', visible=False),
            sg.T("Номер заказа:", **text_setting),
            sg.Push(),
            sg.Combo(
                all_order,
                key='order',
                default_value=task.order if task else 'Не выбрано',
                disabled=True if task else False,
                enable_events=True,
                **drop_down_setting)
        ], [
            sg.T("Тип объекта:", **text_setting),
            sg.Push(),
            sg.Input(task.order.type_obj if task else '', key='type_obj', readonly=True, **input_setting)
        ], [
            sg.T("Наименование:", **text_setting),
            sg.Push(),
            sg.Input(task.order.title if task else '', key='title', readonly=True, **input_setting)
        ], [
            sg.T("Конструктив:", **text_setting),
            sg.Push(),
            sg.Input(task.order.article if task else '', key='article', readonly=True, **input_setting)
        ]], pad=10)]], **frame_setting)], [
        sg.Frame('Задача:', [[sg.Col([
            [
                sg.T("Исполнитель:", **text_setting),
                sg.Push(),
                sg.Combo(
                    workers,
                    key='worker',
                    default_value=task.worker if task else 'Не выбрано',
                    disabled=True if task else False,
                    **drop_down_setting)
            ], [
                sg.T("Отработано:", **text_setting),
                sg.Push(),
                sg.Input(data.get('passed', 0), key='-PASSED-', readonly=True, **input_setting)
            ], [
                sg.T("Норматив:", **text_setting),
                sg.Push(),
                sg.Input(task.deadline if task else '', key='deadline', **input_setting)
            ], [
                sg.T("Статус:", **text_setting),
                sg.Push(),
                sg.Combo(
                    statuses,
                    key='status',
                    default_value=task.status if task else statuses[0],
                    **drop_down_setting)
            ], [
                sg.T("Комментарии:", **text_setting),
                sg.Push(),
                sg.Multiline(task.comment if task and task.comment else '', key='comment', **multiline_setting)
            ]
        ], pad=10)]], **frame_setting)]] +
                          table, pad=0))
            ]


def get_card_order(data):
    if data:
        order = data.get('order', '')
        tasks = data.get('tasks', [])
        table_heads = ['№', 'Статус', 'Норма', 'Вып.', 'Работник', 'Коммент']
        width_cols = [3, 8, 5, 5, 12, 14]
        table = [[
            sg.Frame('Связанные задачи:', [
                [sg.Input(order.id, key='order_id', visible=False)],
                [
                    sg.Table(
                        get_list_task_for_order(tasks),
                        table_heads,
                        col_widths=width_cols,
                        num_rows=5,
                        key='-DOUBLE-TASKS-',
                        **table_setting
                    )
                ]
            ], size=(330, 160), **frame_setting)
        ]]
    else:
        table = []
        order = None

    return [sg.pin(sg.Col([[
        sg.Frame('Заказ:', [[sg.Col([[
            sg.Input('order', key='type', visible=False),
            sg.T("Номер заказа:", **text_setting),
            sg.Push(),
            sg.Input(order.to_order if data else '', key='no', **input_setting)
        ], [
            sg.T("Тип объекта:", **text_setting),
            sg.Push(),
            sg.Input(order.type_obj if data else '', key='type_obj', **input_setting)
        ], [
            sg.T("Наименование:", **text_setting),
            sg.Push(),
            sg.Input(order.title if data else '', key='title', **input_setting)
        ], [
            sg.T("Конструктив:", **text_setting),
            sg.Push(),
            sg.Input(order.article if data else '', key='article', **input_setting)
        ]], pad=10)]], **frame_setting)
    ]] + table, pad=0))
    ]
