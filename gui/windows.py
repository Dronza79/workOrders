import datetime

from database.models import Month
from database.queries import get_all_workers, get_workers_for_list, get_list_years, get_query_reg, get_query_sys
from database.utils import validation_data_for_exel
from .components import get_sector_workers, get_sector_tasks, get_sector_orders, reg_tab_layout, sys_tab_layout
from .templates_settings import *


def get_main_window():
    menu_def = [['Отчеты Exel', MENU_REPORTS]] + [["База данных", MENU_BD]] + [["Настройки", MENU_SETTINGS]]
    menu_right_button = ["", (MENU_RIGHT_MOUSE + ['---'] + ['Отчеты', MENU_REPORTS])]

    layout = [
        [
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
    return sg.Window(
        'Учет работ ЭнергоЭра', layout,
        resizable=True,
        finalize=True,
        return_keyboard_events=True,
        right_click_menu=menu_right_button,
        icon=logo_b,
    )


def get_menu_setting_window():
    reg_data = get_query_reg()
    sys_data = get_query_sys()
    layout = [[
        sg.TabGroup([[
            sg.Tab('Учетные  ', reg_tab_layout(**reg_data), key="REG", **param_tab),
            sg.Tab('Системные', sys_tab_layout(sys_data), key='SYS', **param_tab),
            sg.Tab('Адм.     ', [[sg.Col([[sg.T('все все увидят что им не подложено')]], k='secret', visible=False)]],
                   key='ADM', **param_tab)  # тут удаленные (скрытые вещи)
        ]], key='TG', **param_grouptab)
    ]]
    return sg.Window(
        'Параметры', layout,
        finalize=True,
        keep_on_top=True,
        icon=logo_b,
        margins=(0, 0),
    )


def popup_inter_pass():
    layout = [
        [sg.I(password_char='*', s=10, font='courier', key='PASS', justification='c')],
        [sg.B('OK', expand_x=True)],
    ]
    ev, val = sg.Window('', layout, finalize=True, keep_on_top=True, modal=True).read(close=True)
    return val['PASS'] == '1102' if ev else None


def get_card_window(form):
    title = (
        'Карточка работника' if form in ['-WRK-', '-DSMS-']
        else "Карточка работы" if form in ['-CLS-', '-TSK-']
        else "Карточка заказа"
    )
    rbm = ['', ['Осторожно!...', [f'Удалить{sg.MENU_KEY_SEPARATOR}-DELETE-']]]
    layout = [[
        sg.Col([], key='body', expand_y=True)
    ], [
        sg.Push(),
        sg.Button('Сохранить', key='-SAVE-', focus=True, bind_return_key=True, pad=((0, 5), (10, 10))),
        sg.Button('Отменить', key='-CANCEL-', pad=((5, 0), (10, 10))),
        sg.Push(),
    ], [sg.Push(), sg.Sizegrip()]
    ]
    return sg.Window(
        title, layout, resizable=True,
        return_keyboard_events=True,
        finalize=True,
        keep_on_top=True,
        right_click_menu=rbm,
        margins=(0, 0),
        icon=logo_b
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
                       **get_data_popup_setting)
    move_window(parent, window)
    window['-CB-'].calendar_location = window.current_location()
    while True:
        ev, result = window.read()
        if ev in [sg.WIN_CLOSED, 'Escape:27', '-SAVE-PER-', '-DEL-PER-', '-EXIT-']:
            window.close()
            break
    return ev, result


def popup_choice_worker_for_exel(parent):
    workers = get_workers_for_list()
    list_years = get_list_years()
    layout = [[
        sg.Frame('', [[
            sg.Col([[
                sg.T('Работник:', font='_ 10'),
                sg.Push(),
                sg.Combo(
                    [worker for worker in workers],
                    key='-worker-', **search_drop_down_setting),
            ], [
                sg.T('Отчетный период:', font='_ 10'),
                sg.Push(),
                sg.Combo([Month(num) for num in range(1, 13)],
                         default_value=Month(datetime.datetime.now().month),
                         key='-month-', **drop_down_read_only_setting),
                sg.Combo(list_years, default_value=list_years[-1],
                         key='-year-', **drop_down_read_only_setting),
            ], [
                sg.Push(),
                sg.Button('Создать...', key='-CREATE-', size=(10, 1), pad=((10, 10), (10, 0))),
                sg.Button('Выход', key='-CANCEL-', size=(10, 1), pad=((10, 10), (10, 0))),
                sg.Push()

            ]], pad=15, vertical_alignment='center')]], **frame_setting)
    ]]
    window = sg.Window('Отчет Exel...', layout, finalize=True, modal=True, grab_anywhere=True,
                       return_keyboard_events=True, margins=(0, 0),  # no_titlebar=True,
                       )
    move_window(parent, window)
    while True:
        ev, val = window.read()
        print(f'popup_choice_worker_for_exel {ev=} {val=}')
        if ev in ['-CANCEL-', sg.WIN_CLOSED, 'Escape:27']:
            window.close()
            return
        if ev == '-worker-' and isinstance(val[ev], str):
            new_list_workers = [worker for worker in workers if val[ev].lower() in str(worker).lower()]
            window[ev].update(new_list_workers[0] if new_list_workers else [], values=new_list_workers)
        if ev in ['-CREATE-', '\r']:
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
    list_years = get_list_years()
    layout = [[
        sg.Frame('', [[
            sg.Col([[
                sg.T('Отчетный месяц:', font='_ 10'),
                sg.Push(),
                sg.Combo([Month(num) for num in range(1, 13)],
                         default_value=Month(datetime.datetime.now().month),
                         key='-MONTH-', **drop_down_read_only_setting),
            ], [
                sg.T('Отчетный год:', font='_ 10'),
                sg.Push(),
                sg.Combo(list_years, default_value=list_years[-1],
                         key='-YEAR-', **drop_down_read_only_setting),
            ]], pad=15, vertical_alignment='c')
        ], [
            sg.Push(),
            sg.Button('Создать...', key='-CREATE-', size=(10, 1), pad=((0, 10), (0, 15))),
            sg.Button('Отмена', key='-CANCEL-', size=(10, 1), pad=((10, 0), (0, 15))),
            sg.Push()
        ]], **frame_padding_0_setting)
    ]]
    window = sg.Window('Отчет Exel...', layout, finalize=True, modal=True,
                       return_keyboard_events=True, margins=(0, 0),  # no_titlebar=True,
                       )
    move_window(parent, window)
    while True:
        ev, val = window.read()
        if ev in ['-CANCEL-', sg.WIN_CLOSED, 'Escape:27', '-CREATE-']:
            window.close()
            break
    return {'month': Month(val['-MONTH-'].number, val['-YEAR-'])}


def popup_find_string(parent):
    layout = [[sg.Frame('', [[sg.Col([[
        sg.Text('Найти...', font="_ 14", text_color=sg.DEFAULT_BUTTON_COLOR[1]),
        sg.Input(key='-IN-', **input_setting)
    ]], pad=5)]], **frame_padding_0_setting)]]

    window = sg.Window('Найти...', layout,
                       **get_data_popup_setting)
    move_window(parent, window)
    while True:
        button, values = window.read()
        print(f'{button=} {values=}')
        if button == '\r':
            search = values['-IN-']
            break
        elif button in ['Escape:27', 'Cancel']:
            search = None
            break
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
        if ev == sg.WIN_CLOSED:
            break
        return
    window.close()
    return
