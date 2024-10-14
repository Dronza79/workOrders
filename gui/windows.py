import datetime

import PySimpleGUI as sg

from database.models import Month
from database.queries import get_all_workers
from database.utils import validation_data_for_exel
from .components import get_sector_workers, get_sector_tasks, get_sector_orders
from .templates_settings import (
    tab_setting, drop_down_setting, error_popup_setting,
    frame_setting, tab_group_setting, input_setting, drop_down_read_only_setting, search_drop_down_setting
)


def get_main_window():
    menu_def = [[
        'Файл', [
            f'Сделать бекап{sg.MENU_KEY_SEPARATOR}-BACKUP-',
            f'Указать базу{sg.MENU_KEY_SEPARATOR}-SET-DB-'
        ]], [
        'Отчеты Exel', [
            f'Персональный отчет за период{sg.MENU_KEY_SEPARATOR}-EXEL-',
            f'Общий отчет за месяц{sg.MENU_KEY_SEPARATOR}-MONTH-',
        ]], [
        'Параметры', [
            f'Выбрать тему{sg.MENU_KEY_SEPARATOR}-THEME-',
        ]]
    ]
    layout = [[
        sg.TabGroup([[
            sg.Tab(
                'Список работников',
                get_sector_workers(code='-WORKERS-'),
                key='-WRK-', **tab_setting),
            sg.Tab(
                'Список выполняемых работ',
                get_sector_tasks(code='-TASKS-'),
                key='-TSK-', **tab_setting),
            sg.Tab(
                'Список открытых заказов (ПРки)',
                get_sector_orders(),
                key='-ORD-', **tab_setting),
            sg.Tab(
                'Архив выполненных работ',
                get_sector_tasks(code='-CLOSE-'),
                key='-CLS-', **tab_setting),
            sg.Tab(
                'Исключенные работники',
                get_sector_workers(code='-DISMISS-'),
                key='-DSMS-', **tab_setting),
        ]], key='-TG-', **tab_group_setting)
    ], [
        sg.Button('Добавить', key='-ADD-'),
        sg.Button('Обновить', key='-UPDATE-'),
    ], [
        sg.Menu(menu_def, key='-MENU-')
    ]]
    return sg.Window('Учет нарядов', layout,
                     resizable=True,
                     finalize=True,
                     return_keyboard_events=True,
                     right_click_menu=["", ['Найти...::-FIND-']],
                     sbar_frame_color='#64778D', margins=(10, 10)
                     )


def get_card_window(form):
    title = (
        'Карточка работника' if form in ['-WRK-', '-DSMS-']
        else "Карточка задачи" if form in ['-CLS-', '-TSK-']
        else "Карточка заказа"
    )
    layout = [
        [sg.Col([], key='body')],
        [
            sg.Push(),
            sg.Button('Сохранить', key='-SAVE-', focus=True, bind_return_key=True),
            sg.Button('Отменить', key='-CANCEL-'),
            sg.Push(),
        ]
    ]
    return sg.Window(title, layout,
                     # resizable=True,
                     return_keyboard_events=True,
                     finalize=True,
                     sbar_frame_color='#64778D',
                     # size=(450, 570),
                     margins=(10, 10),
                     # modal=True
                     )


def move_window(parent, window):
    size_w, size_h = parent.current_size_accurate()
    loc_x, loc_y = parent.current_location()
    size = window.current_size_accurate()
    window_location = loc_x + size_w // 2 - size[0] // 2, loc_y + size_h // 2 - size[1] // 2
    window.move(*window_location)
    window.refresh()


def popup_get_period(parent, period=None):
    date_now = datetime.datetime.now().date()
    layout = [
        [
            sg.Input(
                default_text=f'{period.date:%d.%m.%Y}' if period else f'{date_now:%d.%m.%Y}',
                key='date', size=(10, 1)),
            sg.CalendarButton('Календарь', key='-CB-', begin_at_sunday_plus=1, target='date', format='%d.%m.%Y')
        ], [
            sg.T('Продолжительность', font='_ 10'),
            sg.Combo(
                [i for i in range(1, 13)],
                default_value=period.value if period else 1,
                key='value', font='_ 12'),
            sg.T('ч.', font='_ 12')
        ], [sg.Button('Сохранить', key='-SAVE-PER-')] +
           (
               [
                   sg.Button('Удалить', key='-DEL-PER-'),
                   sg.Input(period.id, key='period_id', visible=False)
               ] if period else []
           ) +
           [sg.Exit('Отмена')]
    ]
    window = sg.Window('Добавить время', layout, finalize=True, modal=True)
    move_window(parent, window)
    window['-CB-'].calendar_location = window.current_location()
    return window.read(close=True)


def popup_choice_worker_for_exel(parent):
    workers = get_all_workers()
    layout = [[sg.Frame('', [[sg.Col([
        [
            sg.T('Работник:', font='_ 10'),
            sg.Push(),
            sg.Combo(
                [worker for worker in workers],
                key='-worker-', **search_drop_down_setting),
        ], [
            sg.T('Отчетный месяц:', font='_ 10'),
            sg.Push(),
            sg.Combo(
                [Month(num) for num in range(1, 13)],
                default_value=Month(datetime.datetime.now().month),
                key='-month-', **drop_down_read_only_setting),
        ]], pad=15, vertical_alignment='center')]], **frame_setting)],
              [sg.Push(), sg.Button('Создать...', key='-CREATE-', size=(15, 1), pad=((0, 0), (0, 10))), sg.Push()]
              ]
    window = sg.Window('Отчет Exel...', layout, finalize=True, margins=(10, 10), modal=True)
    move_window(parent, window)
    while True:
        ev, val = window.read()
        # print(f'popup_choice_worker_for_exel {ev=} {val=}')
        if ev == sg.WIN_CLOSED:
            window.close()
            return
        if ev == '-worker-':
            new_list_workers = [worker for worker in workers if val[ev].lower() in str(worker).lower()]
            window[ev].update(new_list_workers[0] if new_list_workers else [], values=new_list_workers)
        if ev == '-CREATE-':
            errors, valid_data = validation_data_for_exel(val)
            if errors:
                sg.popup('\n'.join(errors), title='Ошибка', **error_popup_setting)
            else:
                window.close()
                del window
                break

    return valid_data


def popup_find_string(parent):
    layout = [
        [
            sg.Image(background_color='#99B7D8', size=(32, 32),
                     source=b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAKfSURBVFhHxZbdiw1hHMefIbZzFEXnaLlRi43adkMuXJCVrOJGSZK8S7b2D5A7NteuqL2htDeSUt7CDYWQUijthUVK6yVse7Zla3x+z/MbO3NmjzPzcNanPv2eeeac+T7zPPMWmH9EWCzPoBTdRjgSjH4ct+06eA8gLJYIDFbR3IircRHOQTnmF3yCfUFl6AG1JrkHwJmWKXtwN7ZJXx2OMYhT2k6ReQAEN1OO4iGcL3052Mwgbmg7Qd0BEDyb0qOWpK+KAXyIz3AIZRkOYAdG9DOAXdpO8McBEL6TcgJbbMcEn/AS9uNjDj4qnRH8bznlKTbZDmPu8pt12k4wTWsCDrAYr9CUgHi4nOFxbOOAR1AOnAhXvuKYa1q+aU2RGgDBeylyBW+1HROcwQ4Ce/GD66rJWpSli7itNUViCQifRXmN8bWWsH2ETnoRVcMx5lHu41LbYcwbXMH/5dZMkZgBfjRCOee2LC+wM3u4PBvMBYzCQ+yuFV4TzmIL9ujZZCIslAv8/jKGMffr7sZCUDPeiwWPoTyoGg9B7TigweJ33KC7GwtBnfhZg8Vh3KS7GwtBXVjRYPE9rtHdmcn9MhIIWkKRx+9c22HMO+zian/pNrMz6ZMwA70YhVdwu0+4F5x9C8an/qTu8sJnBuRFU3BNy3WtXvgM4KfWiOlavfAZgKz1sGtaVmr1IvcAuNjeUu64LcsO3gHes+B7F5zVKvBhGsgHqRdeA2AWblIuui1zjc9weQ5MLdx+TdgeFkoztev/8TeD8L0GLMzAerxlguA59Sq26q7GQ9g2HMfoiSj26e7MeM0AQfIeOI3Vt598NefCdwkW4ELX/I18903NDMAgvnJNyw88yO0p/bnw+h4QWIZllMMod8B5wh9Jfz6M+QUWludk9x6IfQAAAABJRU5ErkJggg=='),
            sg.Text('Найти...', background_color='#99B7D8', font="_ 14", text_color="red"),
            sg.Input(
                key='-IN-',
                # pad=((0, 0), (15, 15)),
                **input_setting)
        ], [
            # sg.OK(bind_return_key=True, size=(10, 1)), sg.Cancel(size=(10, 1))
        ]
    ]
    window = sg.Window(
        'Найти...', layout,
        auto_size_text=True,
        no_titlebar=True,
        grab_anywhere=True,
        keep_on_top=True,
        background_color='#99B7D8',
        element_padding=((5, 5), (5, 5)),
        finalize=True,
        # modal=True,
        return_keyboard_events=True,
        # margins=(20, 20),
    )
    move_window(parent, window)
    while True:
        button, values = window.read()
        print(f'{button=} {values=}')
        # if button == 'OK':
        if button == '\r':
            search = values['-IN-']
            break
        elif button in ['Escape:27', 'Cancel']:
            search = None
            break
    window.close()
    return search
