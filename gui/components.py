import PySimpleGUI as sg

from .template_setting import table_setting


def get_sector_workers():
    heads = ['№ п/п', 'Фамилия имя отчество', 'Должность', 'Номер ПР', 'Норматив', 'Срок работы']
    width_cols = [4, 30, 10, 10, 10, 10]
    return [[
        sg.Table(
            values=[],
            headings=heads,
            key='-WORKER-',
            col_widths=width_cols,
            **table_setting)
    ]]


def get_sector_tasks():
    heads = [
        '№ п/п', 'Тип оборудования', 'Наименование объекта',
        'Конструктив', 'Номер ПР', 'Норматив выполнения', 'Время производства', "Работник"]
    width_cols = [4, 5, 5, 5, 5, 5, 5, 5]
    return [[
        sg.Table(
            values=[], headings=heads, key='-TASK-',
            col_widths=width_cols,
            **table_setting)
    ]]
