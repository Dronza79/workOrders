import PySimpleGUI as sg

from .templates_settings import table_setting, input_setting, drop_down_setting, text_setting, multiline_setting


def get_sector_workers():
    heads = ['№ п/п', 'Фамилия имя отчество', 'Должность', 'Номер ПР', 'Норматив', 'Отработано']
    width_cols = [4, 30, 16, 10, 7, 7]
    return [[
        sg.Table(
            values=[],
            headings=heads,
            key='-WORKERS-',
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


def get_card_worker(data):
    job_list = list(data['func_position'])
    worker = data.get('worker')
    table_heads = ['№', 'Объект', 'Артикул', 'ПРка', 'Статус', 'Норма', 'Вып.', 'Коммент']
    width_cols = [3, 12, 20, 10, 8, 5, 5, 14]
    if worker:
        table = (
            [sg.HorizontalSeparator(pad=(0, 30))],
            [sg.Table([
                [i, task.order.title, task.order.article,
                 task.order, task.status, task.deadline, task.worked_out, task.comment, task.id]
                for i, task in enumerate(worker.tasks, start=1)],
                table_heads,
                col_widths=width_cols,
                num_rows=5,
                **table_setting)
            ])
    else:
        table = ([])
    return [[
        sg.Col([
            [
                sg.T("Фамилия:", **text_setting),
                # sg.Push(),
                sg.Input(worker.surname.upper() if worker else '', key='surname', **input_setting)
            ], [
                sg.T("Имя:", **text_setting),
                # sg.Push(),
                sg.Input(worker.name if worker else '', key='name', **input_setting)
            ], [
                sg.T("Отчество:", **text_setting),
                # sg.Push(),
                sg.Input(worker.second_name if worker else '', key='second_name', **input_setting)
            ], [
                sg.HorizontalSeparator(pad=(0, 30))
            ],  [
                sg.T('Табельный номер:', **text_setting),
                # sg.Push(),
                sg.Input(worker.table_num if worker else '', key='tab_num', **input_setting)
            ], [
                sg.T('Должность:', **text_setting),
                # sg.Push(),
                sg.Combo(
                    job_list,
                    key='function',
                    default_value=worker.function.post if worker else 'Не выбрано',
                    **drop_down_setting)
            ], *table
        ], pad=10)
    ]]


def get_card_task(data):
    # task = data.get('task')
    if task := data.get('task'):
        task = task.get()
    statuses = list(data.get('statuses', []))
    workers = list(data.get('workers', []))
    all_order = list(data.get('all_orders', []))
    # print(f'{task=}')
    # print(f'{statuses=}')
    # print(f'{workers=}')
    # print(f'{all_order=}')
    return [[
        sg.Col([
            [
                sg.T("Производственный заказ:", **text_setting),
                # sg.Push(),
                sg.Combo(
                    all_order,
                    key='order',
                    default_value=task.order if task else 'Не выбрано',
                    disabled=True if task else False,
                    enable_events=True,
                    **drop_down_setting)
            ], [
                sg.T("Тип объекта:", **text_setting),
                # sg.Push(),
                sg.Input(task.order.type_obj if task else '', key='type_obj', readonly=True, **input_setting)
            ], [
                sg.T("Наименование объекта:", **text_setting),
                # sg.Push(),
                sg.Input(task.order.title if task else '', key='title', readonly=True, **input_setting)
            ], [
                sg.T("Конструктив:", **text_setting),
                # sg.Push(),
                sg.Input(task.order.article if task else '', key='article', readonly=True, **input_setting)
            ], [
                sg.T("Норматив выполнения:", **text_setting),
                # sg.Push(),
                sg.Input(task.deadline if task else '', key='deadline', **input_setting)
            ], [
                sg.T("Статус:", **text_setting),
                # sg.Push(),
                sg.Combo(
                    statuses,
                    key='status',
                    default_value=task.status.state if task else 'Не выбрано',
                    # disabled=True if task else False,
                    **drop_down_setting)
            ], [
                sg.T("Исполнитель:", **text_setting),
                # sg.Push(),
                sg.Combo(
                    workers,
                    key='master',
                    default_value=task.worker if task else 'Не выбрано',
                    disabled=True if task else False,
                    **drop_down_setting)
            ], [
                sg.T("Комментарии:", **text_setting),
                # sg.Push(),
                sg.Multiline(task.comment if task and task.comment else '', key='comment', **multiline_setting)
            ],
        ], pad=10)
    ]]
