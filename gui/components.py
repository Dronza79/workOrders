import PySimpleGUI as sg

from .templates_settings import table_setting


def get_sector_workers():
    heads = ['№ п/п', 'Фамилия имя отчество', 'Должность', 'Номер ПР', 'Норматив', 'Выпонено']
    width_cols = [4, 30, 10, 10, 10, 10]
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
        '№ п/п', 'Номинал', 'Наименование объекта',
        'Конструктив', 'Номер ПР', 'Норматив', 'Выполнено', "Работник", 'Статус']
    width_cols = [3, 10, 15, 20, 10, 5, 5, 15, 10]
    return [[
        sg.Table(
            values=[], headings=heads, key=code,
            col_widths=width_cols,
            visible_column_map=visible,
            **table_setting)
    ]]

# mounter - монтажник
# fitter - слесарь