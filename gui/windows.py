import PySimpleGUI as sg

from .components import get_sector_workers, get_sector_tasks
from .template_setting import tab_setting


def get_main_window():
    layout = [[
        sg.TabGroup([[
            sg.Tab('Список работников', get_sector_workers(), key='-TW-',
                   **tab_setting),
            sg.Tab('Список монтажных работ', get_sector_tasks(code='-TASK-M-'), key='-TTM-',
                   **tab_setting),
            sg.Tab('Список слесарных работ', get_sector_tasks(code='-TASK-F-'), key='-TTF-',
                   **tab_setting),
        ]], key='-TG-', expand_x=True, expand_y=True)
    ]]
    return sg.Window('Учет нарядов', layout,
                     resizable=True,
                     finalize=True,
                     sbar_frame_color='#64778D', margins=(10, 10)
                     )
