import PySimpleGUI as sg

from database.app_logger import add_logger_peewee
from database.queries import get_all_workers, get_all_tasks
from .windows import get_main_window


class StartMainWindow:
    def __init__(self):
        self.window = get_main_window()
        self.workers = []
        self.tasks = []

    def run(self):
        while True:
            ev, val = self.window.read()
            print(f'{ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            self.actualizing()
        self.window.close()

    @add_logger_peewee
    def actualizing(self):
        self.workers = list(
            [[i, worker, worker.function, worker.tasks[-1], worker.tasks[-1].duration]
             for i, worker in enumerate(get_all_workers(), start=1)])
        self.tasks = get_all_tasks()
        print(f'{self.workers=}')
        self.window['-WORKER-'].update(values=self.workers)

    def get_format_list_workers(self):
        for i, worker in enumerate(get_all_workers(), start=1):
            formatted_data = (
                i,
                f'{worker.surname} {worker.name} {worker.second_name}',
                worker.function.title,

            )

