import PySimpleGUI as sg

from .components import get_sector_workers, get_sector_tasks  #, get_card_worker, get_card_task
from .templates_settings import tab_setting


def get_main_window():
    # visio_arj = [True, True, True, True, True, True, True, False]
    visio_arj = None
    layout = [[
        sg.TabGroup([[
            sg.Tab(
                'Список работников',
                get_sector_workers(),
                key='-TW-', **tab_setting),
            sg.Tab(
                'Список монтажных работ',
                get_sector_tasks(code='-TASK-M-'),
                key='-TTM-', **tab_setting),
            sg.Tab(
                'Список слесарных работ',
                get_sector_tasks(code='-TASK-F-'),
                key='-TTF-', **tab_setting),
            sg.Tab(
                'Архив выполненых работ',
                get_sector_tasks(code='-CLOSE-', visible=visio_arj),
                key='-TTC-', **tab_setting),
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
    layout = [[sg.Col([[]], key='body')]]
    return sg.Window(title, layout,
                     resizable=True,
                     finalize=True,
                     sbar_frame_color='#64778D', margins=(10, 10),
                     modal=True
                     )
