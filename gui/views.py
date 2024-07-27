import PySimpleGUI as sg

from database.app_logger import add_logger_peewee
from database.queries import get_all_workers  # , get_all_tasks
from .windows import get_main_window


class StartMainWindow:
    workers = []
    tasks = []

    def __init__(self):
        self.window = get_main_window()

    def run(self):
        while True:
            ev, val = self.window.read()
            print(f'{ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            self.actualizing()
        self.window.close()

    def actualizing(self):
        self.get_format_list_workers()
        self.window['-WORKER-'].c
        self.window['-WORKER-'].update(values=self.workers)

    @add_logger_peewee
    def get_format_list_workers(self):
        workers = get_all_workers()
        if workers:
            for i, worker in enumerate(workers, start=1):
                formatted_data = (
                    i,
                    f'{worker.surname} {worker.name} {worker.second_name}',
                    worker.function.title,
                    worker.tasks[-1].order,
                    worker.tasks[-1].deadline,
                    worker.tasks[-1].duration,
                    worker.id
                )
                print(f'{formatted_data=}')
                self.workers.append(formatted_data)

