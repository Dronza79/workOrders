import PySimpleGUI as sg

from .components import get_sector_workers, get_sector_tasks
from .template_setting import tab_setting


def get_main_window():
    layout = [[
        sg.TabGroup([[
            sg.Tab('Список работников', get_sector_workers(), key='-TW-',
                   **tab_setting),
            sg.Tab('Список активных работ', get_sector_tasks(), key='-TT-',
                   **tab_setting),
        ]],
            enable_events=True, key='-TG-', expand_x=True, expand_y=True,)
    ]]
    return sg.Window('Учет нарядов', layout,
                     resizable=True,
                     finalize=True,
                     # size=(1000, 700),
                     # use_custom_titlebar=False, titlebar_background_color='#64778D',
                     sbar_frame_color='#64778D', margins=(10, 10)
                     )
