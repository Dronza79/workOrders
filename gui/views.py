from operator import itemgetter

import PySimpleGUI as sg

from database.queries import get_all_workers, get_mounter_tasks, get_fitter_tasks, get_close_tasks
from .windows import get_main_window


class StartMainWindow:
    workers = []
    tasks_mounter = []
    tasks_fitter = []
    tasks_close = []
    sort = False

    def __init__(self):
        self.window = get_main_window()
        self.actualizing()

    def run(self):
        while True:
            ev, val = self.window.read()
            print(f'{type(ev)=} {ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            elif ev == '-TG-':
                self.actualizing()
            elif isinstance(ev, tuple) and ev[2][0] == -1:
                self.sorting_list(ev[0], ev[2][1])
        self.window.close()

    def sorting_list(self, key_table, column):
        self.sort = not self.sort
        table = (
            self.workers if key_table == '-WORKER-'
            else self.tasks_mounter if key_table == '-TASK-M-'
            else self.tasks_fitter if key_table == '-TASK-F-'
            else self.tasks_close
        )
        table = sorted(table, key=itemgetter(column), reverse=self.sort)
        self.window[key_table].update(values=table)

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
                    str(worker.function),
                    task[-1].order if task else '--',
                    task[-1].deadline if task else 0,
                    task[-1].total if task and task[-1].total else 0,
                    worker.id
                )
                self.workers.append(formatted_data)
        print(f'{self.workers=}')


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
        print(f'{self.tasks_mounter=}')
        print(f'{self.tasks_fitter=}')
        print(f'{self.tasks_close=}')
