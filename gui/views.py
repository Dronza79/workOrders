import PySimpleGUI as sg

from database.app_logger import add_logger_peewee
from database.queries import get_all_workers, get_mounter_tasks, get_fitter_tasks, get_close_tasks
from .windows import get_main_window


class StartMainWindow:
    workers = []
    tasks_mounter = []
    tasks_fitter = []
    tasks_close = []

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
        self.window['-CLOSE-'].update(values=self.tasks_close)

    # @add_logger_peewee
    def get_format_list_workers(self):
        all_workers = get_all_workers()
        self.workers = []
        # print(f'{all_workers=}')
        if all_workers:
            for i, worker in enumerate(all_workers, start=1):
                task = worker.tasks
                # print(f'{worker=} {task=} ')
                formatted_data = (
                    i,
                    f'{worker.surname} {worker.name} {worker.second_name}',
                    worker.function,
                    task[-1].order if task else '-',
                    task[-1].deadline if task else '-',
                    task[-1].total if task else '-',
                    worker.id
                )
                self.workers.append(formatted_data)

    @staticmethod
    def _format_list_task(list_task):
        if not list_task:
            return []
        lst = []
        for task in list_task:
            formatted_data = [
                task.type_obj,
                task.title,
                task.article,
                task.order,
                task.deadline,
                task.total,
                f'{task.master.surname} {task.master.name[:1]}.{task.master.second_name[:1]}.',
                task.status.state,
                task.id,
            ]
            formatted_data.insert(0, len(lst) + 1)
            lst.append(formatted_data)
        return lst

    # @add_logger_peewee
    def get_format_list_tasks(self):
        self.tasks_mounter = []
        self.tasks_fitter = []
        self.tasks_close = []
        self.tasks_mounter.extend(self._format_list_task(get_mounter_tasks()))
        self.tasks_fitter.extend(self._format_list_task(get_fitter_tasks()))
        self.tasks_close.extend(self._format_list_task(get_close_tasks()))
