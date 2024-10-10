import datetime

import PySimpleGUI as sg

from database.queries import get_all_workers
from database.utils import validation_data_for_exel
from .components import get_sector_workers, get_sector_tasks, get_sector_orders
from .templates_settings import tab_setting, calendar_button_setting, drop_down_setting, error_popup_setting, \
    frame_setting, tab_group_setting


def get_main_window():
    menu_def = [[
        'Файл', [
            f'Вывести отчет в Exel{sg.MENU_KEY_SEPARATOR}-EXEL-',
            f'Сделать бекап{sg.MENU_KEY_SEPARATOR}-BACKUP-'
        ]], [
        'Параметры', [
            f'Выбрать тему{sg.MENU_KEY_SEPARATOR}-THEME-',
            f'Выбрать базу{sg.MENU_KEY_SEPARATOR}-SET-DB-'
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
            sg.Combo(
                [worker for worker in workers],
                default_value=workers[0],
                key='-worker-', **drop_down_setting),
        ], [
            sg.T('от', font='_ 10'),
            sg.Input(
                key='-from-', size=(10, 1)),
            sg.CalendarButton(key='-B-FROM-',
                              **calendar_button_setting)
        ], [
            sg.T('по', font='_ 10'),
            sg.Input(
                key='-to-', size=(10, 1)),
            sg.CalendarButton(key='-B-TO-',
                              **calendar_button_setting)
        ]], pad=15, vertical_alignment='center')]], **frame_setting)],
        [sg.Push(), sg.Button('Создать...', key='-CREATE-', size=(15, 1), pad=((0, 0), (0, 10))), sg.Push()]
    ]
    window = sg.Window('Отчет Exel...', layout, finalize=True, margins=(10, 10), modal=True)
    move_window(parent, window)
    window['-B-FROM-'].calendar_location = window.current_location()
    window['-B-TO-'].calendar_location = window.current_location()
    while True:
        ev, val = window.read()
        # valid_data = None
        if ev == sg.WIN_CLOSED:
            window.close()
            return
        errors, valid_data = validation_data_for_exel(val)
        if errors:
            sg.popup('\n'.join(errors), title='Ошибка', **error_popup_setting)
        else:
            window.close()
            break

    return valid_data
