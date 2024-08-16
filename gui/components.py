import PySimpleGUI as sg

from .templates_settings import table_setting, input_setting, drop_down_setting, text_setting


def get_sector_workers():
    heads = ['№ п/п', 'Фамилия имя отчество', 'Должность', 'Номер ПР', 'Норматив', 'Выпонено']
    width_cols = [4, 36, 14, 10, 5, 5]
    return [[
        sg.Table(
            values=[],
            headings=heads,
            key='-WORKER-',
            col_widths=width_cols,
            **table_setting)
    ]]


def get_sector_tasks(code='', visible=None):
    heads = [
        '№', 'Номинал', 'Наименование объекта',
        'Конструктив', 'Номер ПР', 'Норма', 'Вып.', "Работник", 'Статус']
    width_cols = [3, 14, 14, 21, 10, 5, 5, 13, 8]
    return [[
        sg.Table(
            values=[], headings=heads, key=code,
            col_widths=width_cols,
            visible_column_map=visible,
            **table_setting)
    ]]


# mounter - монтажник
# fitter - слесарь


def get_card_worker(data):
    job_list = list(data['func_position'])
    worker = data.get('person')
    table_heads = ['№', 'Объект', 'Артикул', 'ПРка', 'Статус']
    width_cols = [3, 10, 20, 10, 8]
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
                    default_value=worker.function.job_name if worker else 'Не выбрано',
                    **drop_down_setting)
            ], [
                sg.HorizontalSeparator(pad=(0, 30))
            ], [
                sg.Table([
                    [i, task.title, task.article, task.order, task.status]
                    for i, task in enumerate(worker.tasks, start=1)], table_heads,
                    col_widths=width_cols,
                    num_rows=5,
                    **table_setting
                )
            ]
        ], pad=10)
    ]]


def get_card_task():
    return [[]]
