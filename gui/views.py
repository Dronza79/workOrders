import PySimpleGUI as sg

from database.app_logger import add_logger_peewee
from database.queries import get_all_workers, get_all_tasks
from .windows import get_main_window


class StartMainWindow:
    workers = []
    tasks = []

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
        self.window['-WORKER-'].update(values=self.workers)
        self.get_format_list_tasks()
        self.window['-TASK-'].update(values=self.tasks)

    @add_logger_peewee
    def get_format_list_workers(self):
        workers = get_all_workers()
        self.workers = []
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

    @add_logger_peewee
    def get_format_list_tasks(self):
        tasks = get_all_tasks()
        self.tasks = []
        if tasks:
            for i, task in enumerate(tasks, start=1):
                formatted_data = (
                    i,
                    task.equipment,
                    task.title,
                    task.article,
                    task.order,
                    task.deadline,
                    task.duration,
                    f'{task.master.surname} {task.master.name[:1]}.{task.master.second_name[:1]}.',
                    task.status.state,
                    task.id,
                )
                print(f'{formatted_data=}')
                # print(task)
                self.tasks.append(formatted_data)
