import datetime

import PySimpleGUI as sg

from database.models import Month
from database.queries import get_all_workers, get_workers_for_list
from database.utils import validation_data_for_exel
from .components import get_sector_workers, get_sector_tasks, get_sector_orders
from .templates_settings import (
    tab_setting, error_popup_setting,
    frame_setting, tab_group_setting, input_setting, drop_down_read_only_setting, search_drop_down_setting, logo_w,
    title_bar_setting, menu_bar_setting, get_data_popup_setting, calendar_button_setting, frame_padding_0_setting,
    logo_b, menu_setting
)


def get_main_window():
    menu_def = [[
        'Отчеты Exel', [
            f'Работы за месяц...{sg.MENU_KEY_SEPARATOR}-EXEL-',
            f'Общий табель за месяц...{sg.MENU_KEY_SEPARATOR}-MONTH-',
        ]], [
        'Настройки', [
            'База данных', [
                f'Сделать бекап{sg.MENU_KEY_SEPARATOR}-BACKUP-',
                f'Выбрать файл базы{sg.MENU_KEY_SEPARATOR}-SET-DB-'
            ],
            f'Выбрать тему...{sg.MENU_KEY_SEPARATOR}-THEME-',
            f'Параметры...{sg.MENU_KEY_SEPARATOR}-SETTING-',
        ]]
    ]
    menu_right_button = ["", ['Найти...::-FIND-', '---', 'Добавить...::-ADD-', 'Обновить...::-UPDATE-', ]]
    layout = [
        [
            #     sg.Titlebar('Учет работ ЭнергоЭра', icon=logo_w, **title_bar_setting)
            # ], [
            #     sg.MenubarCustom(menu_def, key='-MENU-', **menu_bar_setting)
            # ], [
            sg.Menu(menu_def, key='-MENU-', **menu_setting)
        ], [
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
            sg.Button('Добавить', key='-ADD-', pad=((10, 5), (5, 10))),
            sg.Button('Обновить', key='-UPDATE-', pad=((5, 0), (5, 10))),
            sg.Push(),
            sg.Sizegrip()
        ]]
    return sg.Window('Учет работ ЭнергоЭра', layout,
                     resizable=True,
                     finalize=True,
                     return_keyboard_events=True,
                     right_click_menu= menu_right_button,
                     icon=logo_b,
                     )


def get_card_window(form):
    title = (
        'Карточка работника' if form in ['-WRK-', '-DSMS-']
        else "Карточка задачи" if form in ['-CLS-', '-TSK-']
        else "Карточка заказа"
    )
    rbm = ['', ['Осторожно!...', [f'Удалить{sg.MENU_KEY_SEPARATOR}-DELETE-']]]
    layout = [[sg.Frame('', [
        [
            sg.Titlebar(title, icon=logo_w, **title_bar_setting)
        ], [
            sg.Col([], key='body')
        ], [
            sg.Push(),
            sg.Button('Сохранить', key='-SAVE-', focus=True, bind_return_key=True, pad=((0, 5), (0, 20))),
            sg.Button('Отменить', key='-CANCEL-', pad=((5, 0), (0, 20))),
            sg.Push(),
        ]
    ], **frame_padding_0_setting)]]
    return sg.Window(title, layout,
                     # resizable=True,
                     return_keyboard_events=True,
                     finalize=True,
                     keep_on_top=True,
                     right_click_menu=rbm,
                     margins=(10, 10),
                     icon=logo_b
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
    layout = [[sg.Frame('', [
        [
            sg.Titlebar('Добавить время', icon=logo_w, **title_bar_setting)
        ], [sg.Col([[
            sg.Input(
                default_text=f'{period.date:%d.%m.%Y}' if period else f'{date_now:%d.%m.%Y}',
                key='date', size=(15, 1), justification='center'),
            sg.Push(),
            sg.CalendarButton(key='-CB-', target='date', **calendar_button_setting)
        ], [
            sg.T('Продолжительность:', font='_ 10', pad=((5, 5), (5, 20))),
            sg.Push(),
            sg.Combo(
                [i for i in range(1, 13)],
                default_value=period.value if period else 1,
                key='value', font='_ 12', readonly=True, pad=((5, 5), (5, 20))),
            sg.T('ч.', font='_ 12', pad=((5, 5), (5, 20)))
        ], [sg.Button('Сохранить', key='-SAVE-PER-', focus=True, size=(10, 1))] + (
            [
                sg.Push(),
                sg.Button('Удалить', key='-DEL-PER-', size=(10, 1), button_color='white on red'),
                sg.Push(),
                sg.Input(period.id, key='period_id', visible=False)
            ] if period else [sg.Push()]) +
           [sg.Exit('Отмена', key='-EXIT-', size=(10, 1))]
        ], pad=10)]], **frame_padding_0_setting)]]
    window = sg.Window('Добавить время', layout,
                       # element_padding=((15, 15), (5, 10)),
                       no_titlebar=True,
                       **get_data_popup_setting)
    move_window(parent, window)
    window['-CB-'].calendar_location = window.current_location()
    # result = window.read(close=True)
    while True:
        ev, result = window.read()
        # print(f'popup_get_period() {ev=} {result=}')
        if ev in [sg.WIN_CLOSED, 'Escape:27', '-SAVE-PER-', '-DEL-PER-', '-EXIT-']:
            window.close()
            break
    return ev, result


def popup_choice_worker_for_exel(parent):
    workers = get_workers_for_list()
    layout = [
        [
            sg.Titlebar('Отчет Exel...', icon=logo_w, **title_bar_setting)
        ], [
            sg.Frame('', [[sg.Col([[
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
            ]], pad=15, vertical_alignment='center')]], relief=sg.RELIEF_SOLID, border_width=0, **frame_setting)
        ], [
            sg.Push(), sg.Button('Создать...', key='-CREATE-', size=(15, 1), pad=((0, 0), (0, 10))), sg.Push()
        ]
    ]
    window = sg.Window('Отчет Exel...', layout, finalize=True, margins=(20, 20), modal=True)
    move_window(parent, window)
    parent.alpha_channel = .95
    while True:
        ev, val = window.read()
        print(f'popup_choice_worker_for_exel {ev=} {val=}')
        if ev == sg.WIN_CLOSED:
            window.close()
            return
        if ev == '-worker-' and isinstance(val[ev], str):
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

    parent.alpha_channel = 1
    return valid_data


def popup_choice_month_for_exel(parent):
    layout = [[
        sg.Frame('', [[
            sg.Titlebar('Отчет Exel...', icon=logo_w, **title_bar_setting)
        ], [
            sg.Col([[
                sg.T('Отчетный месяц:', font='_ 10'),
                sg.Push(),
                sg.Combo(
                    [Month(num) for num in range(1, 13)],
                    default_value=Month(datetime.datetime.now().month),
                    key='-MONTH-', **drop_down_read_only_setting),
            ]], pad=15, vertical_alignment='center')
        ], [
            sg.Push(), sg.Button('Создать...', key='-CREATE-', size=(15, 1), pad=((0, 0), (0, 10))), sg.Push()
        ]], **frame_padding_0_setting)
    ]]
    window = sg.Window('Отчет Exel...', layout, finalize=True, modal=True)
    move_window(parent, window)
    ev, val = window.read(close=True)
    return val['-MONTH-']


def popup_find_string(parent):
    layout = [[sg.Frame('', [[sg.Col([[
        sg.Text('Найти...', font="_ 14", text_color=sg.DEFAULT_BUTTON_COLOR[1]),
        sg.Input(key='-IN-', **input_setting)
    ]], pad=5)]], **frame_padding_0_setting)]]

    window = sg.Window('Найти...', layout, no_titlebar=True, **get_data_popup_setting)
    move_window(parent, window)
    # parent.alpha_channel = .95
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
    # parent.alpha_channel = 1.0
    window.close()
    return search


def popup_output():
    layout = [[
        sg.Col([[
            sg.Output(size=(50, 20), pad=0, echo_stdout_stderr=True, expand_x=True, expand_y=True)
        ]])
    ]]
    window = sg.Window('Отображение', layout, return_keyboard_events=True)
    while True:
        ev, val = window.read(timeout=100)
        # print(f'popup_output {ev=}, {val=}')
        if ev == sg.WIN_CLOSED:
            break
        return
    window.close()
    return
