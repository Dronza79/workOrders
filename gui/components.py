import PySimpleGUI as sg

from .templates_settings import table_setting, input_setting, drop_down_setting, text_setting, multiline_setting, \
    delete_button_setting, table_period_setting, frame_setting, table_tasks_setting, drop_down_type_task_setting, \
    search_drop_down_setting, input_readonly_setting, drop_down_read_only_setting


def get_sector_workers(code=''):
    heads = ['№ п/п', 'Фамилия имя отчество', 'Таб.номер', 'Должность', 'Работа', 'Номер ПР', 'Норматив', 'Отработано']
    width_cols = [4, 30, 10, 16, 10, 10, 7, 7]
    return [[
        sg.Table(
            values=[],
            headings=heads,
            key=code,
            col_widths=width_cols,
            font='_ 12',
            **table_setting)
    ]]


def get_sector_orders():
    heads = [
        '№', 'Номер ПР', 'Тип', 'Объект', "Конструктив", "Название", 'Норма', 'Выполн.', 'Статус']
    width_cols = [2, 12, 12, 12, 21, 18, 2, 2, 10]
    return [[
        sg.Table(
            values=[], headings=heads, key='-ORDERS-',
            col_widths=width_cols,
            font='_ 11',
            **table_setting)
    ]]


def get_sector_tasks(code=''):
    heads = [
        '№', 'Тип работы', 'Статус', "Работник", 'Норма', 'Вып.', 'Номер ПР', 'Тип', 'Объект', "Название"]
    width_cols = [2, 8, 8, 10, 3, 3, 8, 11, 12, 12]
    return [[
        sg.Table(
            values=[], headings=heads, key=code,
            col_widths=width_cols,
            font='_ 12',
            **table_setting)
    ]]


def get_list_task_for_worker(query):
    # print(f'{__name__}.get_list_task_for_worker({list(query)=})')
    if not query:
        return []
    return [[
        i,
        task.is_type,
        task.deadline,
        task.passed if task.passed else 0,
        task.order if task.order else '-',
        task.order.title if task.order else '-',
        task.order.article if task.order else '-',
        task.comment,
        task.status,
        task.id
    ] for i, task in enumerate(query, start=1)]


def get_list_task_for_order(query):
    if not query:
        return []
    return [[
        i,
        task.status,
        task.deadline,
        task.passed if task.passed else 0,
        task.worker.surname,
        task.comment
    ] for i, task in enumerate(query, start=1)]


def get_card_worker(data):
    # print(f'{__name__}.get_card_worker({data=})')
    job_list = list(data['func_position'])
    worker = data.get('worker')
    tasks = data.get('tasks')
    # print(f'{__name__}.get_card_worker() {list(tasks)=}')
    table_heads = ['№', 'Тип', 'Норма', 'Вып.', 'ПРка', 'Объект', 'Артикул', 'Коммент', 'Статус']
    width_cols = [3, 8, 3, 3, 8, 12, 20, 10, 8]
    rcm = [
        '', [
            f'Добавить задачу...{sg.MENU_KEY_SEPARATOR}-ADD-TASK-',
            f'Найти...{sg.MENU_KEY_SEPARATOR}-FIND-',
            'Внимание!...', [
                f'Удалить{sg.MENU_KEY_SEPARATOR}-DELETE-'
            ]
        ]]
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
            sg.Frame(
                'Задачи выполняемые работником:', [
                    [sg.Input(worker.id, key='id', visible=False)],
                    [sg.Table(
                        get_list_task_for_worker(tasks),
                        table_heads,
                        col_widths=width_cols,
                        num_rows=5,
                        key='-DOUBLE-TASKS-',
                        **table_tasks_setting)]
                ],
                # size=(330, 200),
                right_click_menu=rcm, **frame_setting)
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
            # ], pad=15, vertical_alignment='center')]], **frame_setting)], [
        ], pad=15, vertical_alignment='center')]], **frame_setting),
        sg.Push(),
        sg.Frame('Служебные данные:', [[
            sg.Col([[
                sg.T('Табельный номер:', **text_setting),
                sg.Push(),
                sg.Input(worker.table_num if worker else '', key='table_num', **input_setting)
            ], [
                sg.T('Должность:', **text_setting),
                sg.Push(),
                sg.Combo(
                    job_list,
                    key='function',
                    default_value=worker.function if worker else 'Не выбрано',
                    readonly=True,
                    **drop_down_setting)
            ]] + buttons, pad=10)]], **frame_setting)],
        *table
    ], pad=0))]


def get_card_task(data, prefill):
    print(f'get_card_task({data=}, {prefill=})')
    time_worked = [
        [f'{period.date:%d.%m.%y}',
         f'{period.date:%a}',
         f'{period.value} ч.',
         period.id
         ] for period in data.get('time_worked', [])]
    headers = ['Дата', 'Дн.нед.', 'Время']
    width_cols = [10, 5, 5]
    if task := data.get('task'):
        table = [[
            sg.pin(sg.Frame('Табель времени:', [
                [sg.Input(task.id, key='id', visible=False)],
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
            ], size=(330, 150), **frame_setting))
        ]]
    else:
        table = []
    statuses = list(data.get('statuses', []))
    workers = list(data.get('workers', []))
    all_order = list(data.get('all_orders', []))
    all_types = list(data.get('types', []))
    prefill_worker = None
    prefill_order = None
    if prefill:
        if prefill[0] == 'worker':
            prefill_worker = list(filter(lambda x: x.id == int(prefill[1]), workers)).pop()
        else:
            prefill_order = list(filter(lambda x: x.id == int(prefill[1]), all_order)).pop()

    # print(f'{prefill_worker=} {prefill_order=}')

    if (task and task.is_type.has_extension) or prefill_order:
        extension = True
    else:
        extension = False

    return [sg.pin(
        sg.Col([[
            sg.Frame('Задача:', [[
                sg.Col([[
                    sg.T("Исполнитель:", **text_setting),
                    sg.Push(),
                    sg.Combo(
                        workers,
                        key='worker',
                        default_value=task.worker if task else prefill_worker if prefill_worker else 'Не выбрано',
                        disabled=True if task else False,
                        background_color=sg.DEFAULT_BACKGROUND_COLOR if task else None,
                        **search_drop_down_setting)
                ], [
                    sg.T("Тип задачи:", **text_setting),
                    sg.Push(),
                    sg.Combo(
                        all_types,
                        key='is_type',
                        default_value=task.is_type if task else 'Не выбрано',
                        disabled=True if task else False,
                        background_color=sg.DEFAULT_BACKGROUND_COLOR if task else None,
                        enable_events=True,
                        **drop_down_type_task_setting)
                ], [
                    sg.T("Отработано:", **text_setting),
                    sg.Push(),
                    sg.Input(
                        data.get('passed_order') if data.get('passed_order') else data.get(
                            'passed_task', 0),
                        key='-PASSED-',
                        readonly=True,
                        **input_readonly_setting)
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
                        **drop_down_read_only_setting)
                ], [
                    sg.T("Комментарии:", **text_setting),
                    sg.Push(),
                    sg.Multiline(task.comment if task and task.comment else '', key='comment',
                                 **multiline_setting)
                ]], pad=10)]], **frame_setting)
        ], [
            sg.pin(sg.Frame('Заказ:', [[sg.Col([
                [
                    sg.Input('task', key='type', visible=False),
                    sg.T("Номер заказа:", **text_setting),
                    sg.Push(),
                    sg.Combo(
                        all_order,
                        key='order',
                        default_value=task.order if task and task.order else prefill_order if prefill_order else 'Не выбрано',
                        disabled=True if task else True if prefill_order else False,
                        background_color=sg.DEFAULT_BACKGROUND_COLOR if task else None,
                        **search_drop_down_setting)
                ], [
                    sg.T("Тип объекта:", **text_setting),
                    sg.Push(),
                    sg.Input(
                        task.order.type_obj if task and task.order else prefill_order.type_obj if prefill_order else '',
                        key='type_obj', readonly=True, **input_readonly_setting)
                ], [
                    sg.T("Объект:", **text_setting),
                    sg.Push(),
                    sg.Input(
                        task.order.title if task and task.order else prefill_order.title if prefill_order else '',
                        key='title', readonly=True, **input_readonly_setting)
                ], [
                    sg.T("Конструктив:", **text_setting),
                    sg.Push(),
                    sg.Input(
                        task.order.article if task and task.order else prefill_order.article if prefill_order else '',
                        key='article', readonly=True, **input_readonly_setting)
                ], [
                    sg.T("Название:", **text_setting),
                    sg.Push(),
                    sg.Input(
                        task.order.name if task and task.order else prefill_order.name if prefill_order else '',
                        key='name', readonly=True, **input_readonly_setting)
                ]], pad=10)]],
                            key='-ORDER-TASK-',
                            visible=extension,
                            **frame_setting))
        ]] + table, pad=0))]


def get_card_order(data):
    if data:
        order = data.get('order', '')
        tasks = data.get('tasks', [])
        table_heads = ['№', 'Статус', 'Норма', 'Вып.', 'Работник', 'Коммент']
        width_cols = [3, 8, 5, 5, 12, 14]
        rcm = ['', [
            f'Добавить задачу...{sg.MENU_KEY_SEPARATOR}-ADD-TASK-',
            f'Найти...{sg.MENU_KEY_SEPARATOR}-FIND-',
            'Внимание!...', [
                f'Удалить{sg.MENU_KEY_SEPARATOR}-DELETE-'
            ]
        ]]
        table = [[
            sg.Frame('Задачи с этой ПРкой:', [
                [sg.Input(order.id, key='id', visible=False)],
                [
                    sg.Table(
                        get_list_task_for_order(tasks),
                        table_heads,
                        col_widths=width_cols,
                        num_rows=3,
                        key='-DOUBLE-TASKS-',
                        **table_tasks_setting
                    )
                ]
            ], size=(330, 200), right_click_menu=rcm, **frame_setting)
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
            sg.T("Объект:", **text_setting),
            sg.Push(),
            sg.Input(order.title if data else '', key='title', **input_setting)
        ], [
            sg.T("Конструктив:", **text_setting),
            sg.Push(),
            sg.Input(order.article if data else '', key='article', **input_setting)
        ], [
            sg.T("Название:", **text_setting),
            sg.Push(),
            sg.Input(order.name if data else '', key='name', **input_setting)
        ]], pad=10)]], **frame_setting)
    ]] + table, pad=0))
            ]
