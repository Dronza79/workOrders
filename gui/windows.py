import datetime

import PySimpleGUI as sg

from .components import get_sector_workers, get_sector_tasks, get_sector_orders
from .templates_settings import tab_setting


def get_main_window():
    layout = [[
        sg.TabGroup([[
            sg.Tab(
                'Список работников',
                get_sector_workers(code='-WORKERS-'),
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
            sg.Tab(
                'Исключенные работники',
                get_sector_workers(code='-DISMISS-'),
                key='-DSMS-', **tab_setting),
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
    title = (
        'Карточка работника' if form == '-WRK-'
        else "Карточка задачи" if form in ['-CLS-', '-TSK-']
        else "Карточка заказа"
    )
    layout = [
        [sg.Col([[]], key='body')],
        [sg.Push(), sg.B('Сохранить', key='-SAVE-'), sg.B('Отменить', key='-CANCEL-'), sg.Push()]
    ]
    return sg.Window(title, layout,
                     resizable=True,
                     finalize=True,
                     sbar_frame_color='#64778D',
                     size=(450, 570),
                     margins=(10, 10),
                     # modal=True
                     )


def popup_get_period(parent):
    date_now = datetime.datetime.now().date()
    layout = [
        [
            sg.Input(default_text=f'{date_now:%d.%m.%Y}', key='date', size=(10, 1)),
            sg.CalendarButton('Календарь', key='-CB-', begin_at_sunday_plus=1, target='date', format='%d.%m.%Y')
        ], [
            sg.T('Продолжительность', font='_ 10'),
            sg.Combo([i for i in range(1, 13)], default_value=1, key='value', font='_ 12'),
            sg.T('ч.', font='_ 12')
        ], [
            sg.Button('Сохранить'), sg.Exit('Отмена')
        ]
    ]
    window = sg.Window('Добавить время', layout, finalize=True, modal=True)
    size_w, size_h = parent.current_size_accurate()
    loc_x, loc_y = parent.current_location()
    window.refresh()
    size = window.current_size_accurate()
    window.move(loc_x + size_w // 2 - size[0] // 2, loc_y + size_h // 2 - size[1] // 2)
    window['-CB-'].calendar_location = loc_x + size_w // 2 - size[0] // 2, loc_y + size_h // 2 - size[1] // 2
    return window.read(close=True)[1]
