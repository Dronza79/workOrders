import PySimpleGUI as sg

from database.app_logger import add_logger_peewee
from database.queries import get_all_workers, get_all_tasks
from .windows import get_main_window


class StartMainWindow:
    workers = []
    tasks_mounter = []
    tasks_fitter = []

    def __init__(self):
        self.window = get_main_window()
        self.actualizing()

    def run(self):
        while True:
            ev, val = self.window.read()
            print(f'{ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
        self.window.close()

    def actualizing(self):
        self.get_format_list_workers()
        self.get_format_list_tasks()
        self.window['-WORKER-'].update(values=self.workers)
        self.window['-TASK-M-'].update(values=self.tasks_mounter)
        self.window['-TASK-F-'].update(values=self.tasks_fitter)

    # @add_logger_peewee
    def get_format_list_workers(self):
        all_workers = get_all_workers()
        self.workers = []
        if all_workers:
            for i, worker in enumerate(all_workers, start=1):
                formatted_data = (
                    i,
                    f'{worker["surname"]} {worker["name"]} {worker["second_name"]}',
                    worker['post'],
                    worker['order'],
                    worker['deadline'],
                    worker['total'],
                    worker['id']
                )
                self.workers.append(formatted_data)

    @add_logger_peewee
    def get_format_list_tasks(self):
        tasks = get_all_tasks()
        self.tasks_mounter = []
        self.tasks_fitter = []
        if tasks:
            for task in tasks:
                formatted_data = [
                    task['type_obj'],
                    task['title'],
                    task['article'],
                    task['order'],
                    task['deadline'],
                    task['total'],
                    f'{task["surname"]} {task["name"][:1]}.{task["second_name"][:1]}.',
                    task["state"],
                    task['id'],
                ]
                print(f'{task=}')
                if task['post'] == 'Слесарь':
                    formatted_data.insert(0, len(self.tasks_fitter) + 1)
                    self.tasks_fitter.append(formatted_data)
                else:
                    formatted_data.insert(0, len(self.tasks_mounter) + 1)
                    self.tasks_mounter.append(formatted_data)
