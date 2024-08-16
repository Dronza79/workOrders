import PySimpleGUI as sg

from .templates_settings import table_setting, text_setting, drop_down_setting


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
    print(f'get_card_worker() {worker=}')
    return [[
        sg.Col([
            [
                sg.T("Фамилия:"),
                sg.Push(),
                sg.Input(worker.surname.upper() if worker else '', key='surname', **text_setting)
            ], [
                sg.T("Имя:"),
                sg.Push(),
                sg.Input(worker.name if worker else '', key='name', **text_setting)
            ], [
                sg.T("Отчество:"),
                sg.Push(),
                sg.Input(worker.second_name if worker else '', key='second_name', **text_setting)
            ], [
                sg.HorizontalSeparator(pad=(0, 10))
            ],  [
                sg.T('Табельный номер:'),
                sg.Push(),
                sg.Input(worker.table_num if worker else '', key='tab_num', **text_setting)
            ], [
                sg.T('Должность:'),
                sg.Push(),
                sg.Combo(
                    job_list,
                    key='function',
                    default_value=worker.function.job_name if worker else 'Не выбрано',
                    **drop_down_setting)
            ]
        ], pad=10)
    ]]


def get_card_task():
    return [[]]
