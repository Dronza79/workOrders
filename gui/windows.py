import PySimpleGUI as sg

from .components import get_sector_workers, get_sector_tasks, get_sector_orders
from .templates_settings import tab_setting


def get_main_window():
    layout = [[
        sg.TabGroup([[
            sg.Tab(
                'Список работников',
                get_sector_workers(),
                key='-WRK-', **tab_setting),
            sg.Tab(
                'Список открытых заказов (ПРки)',
                get_sector_orders(),
                key='-ORD-', **tab_setting),
            sg.Tab(
                'Список выполняемых работ',
                get_sector_tasks(code='-TASKS-'),
                key='-TSK-', **tab_setting),
            sg.Tab(
                'Архив выполненных работ',
                get_sector_tasks(code='-CLOSE-'),
                key='-CLS-', **tab_setting),
        ]], key='-TG-', expand_x=True, expand_y=True, enable_events=True)
    ], [
        sg.Button('Добавить', key='-ADD-'),
        sg.Button('Обновить', key='-UPDATE-'),
    ]]
    return sg.Window('Учет нарядов', layout,
                     resizable=True,
                     finalize=True,
                     sbar_frame_color='#64778D', margins=(10, 10)
                     )


def get_card_window(form):
    title = 'Карточка работника' if form == '-TW-' else "Карточка задачи"
    layout = [
        [sg.Col([[]], key='body')],
        [sg.Push(), sg.B('Сохранить', key='-SAVE-'), sg.B('Отменить', key='-CANCEL-'), sg.Push()]
    ]
    return sg.Window(title, layout,
                     resizable=True,
                     finalize=True,
                     sbar_frame_color='#64778D', margins=(10, 10),
                     modal=True
                     )
