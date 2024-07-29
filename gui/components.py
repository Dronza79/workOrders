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


def get_sector_tasks(code=''):
    heads = [
        '№ п/п', 'Номинал', 'Наименование объекта',
        'Конструктив', 'Номер ПР', 'Норма', 'Итого', "Работник"]
    width_cols = [3, 10, 15, 20, 10, 5, 5, 15]
    return [[
        sg.Table(
            values=[], headings=heads, key=code,
            col_widths=width_cols,
            **table_setting)
    ]]

# mounter - монтажник
# fitter - слесарь