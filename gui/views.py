from operator import itemgetter

import PySimpleGUI as sg

from database.queries import get_all_workers, get_mounter_tasks, get_fitter_tasks, get_close_tasks, get_worker_data, \
    get_task_data
from .components import get_card_worker, get_card_task
from .windows import get_main_window, get_card_window


class StartWindowCard:
    def __init__(self, parent, raw_data=None, key=None,):
        self.idx = raw_data[-1] if raw_data else None
        self.key = key
        self.parent = parent
        self.window = get_card_window(form=self.key)
        self.run()

    def run(self):
        if self.key == '-TW-':
            data = get_worker_data(idx=self.idx)
            card = get_card_worker(data)
        else:
            data = get_task_data(idx=self.idx)
            card = get_card_task(data)
        self.window.extend_layout(self.window['body'], card)
        self.move_center()
        while True:
            ev, val = self.window.read()
            print(f'{ev=} {val=}')
            if ev in [sg.WIN_CLOSED, '-CANCEL-']:
                break
        self.window.close()

    def move_center(self):
        size_w, size_h = self.parent.current_size_accurate()
        loc_x, loc_y = self.parent.current_location()
        self.window.refresh()
        size = self.window.current_size_accurate()
        self.window.move(loc_x + size_w // 2 - size[0] // 2, loc_y + size_h // 2 - size[1] // 2)


class StartMainWindow:
    table = {
        '-WORKERS-': [],
        '-ORDERS-': [],
        '-TASKS-': [],
        '-CLOSE-': [],
    }
    sort = False
    sort_col = None

    def __init__(self):
        self.window = get_main_window()
        self.actualizing()
        self.run()

    def run(self):
        while True:
            ev, val = self.window.read()
            print(f'{ev=} {val=}')
            # print(f'{type(ev)=} {ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            elif ev in ['-TG-', '-UPDATE-']:
                self.actualizing()
            elif isinstance(ev, tuple) and ev[2][0] == -1:
                self.sorting_list(ev[0], ev[2][1])
            elif ev in ['-WORKER-', '-TASK-M-', '-TASK-F-', '-CLOSE-', '-ADD-']:
                print(f"{val.get(ev)=}")
                # print(f"{self.table.get(ev)=} {val.get(ev)=}")
                kwargs = {
                    'raw_data': self.table[ev][val[ev].pop()] if val.get(ev) else None,
                    'key': val.get('-TG-'),
                    'parent': self.window
                }
                worker_card = StartWindowCard(**kwargs)
        self.window.close()

    def sorting_list(self, key_table, column):
        if self.sort_col == column:
            self.sort = not self.sort
        # print(f'{self.sort_col=} {self.sort=}')
        self.table[key_table] = sorted(self.table[key_table], key=itemgetter(column), reverse=self.sort)
        self.window[key_table].update(values=self.table[key_table])
        if self.sort_col == column:
            self.sort = not self.sort
        self.sort_col = column
        # print(f'{self.sort_col=} {self.sort=}')

    def actualizing(self):
        self.get_format_list_workers()
        self.get_format_list_tasks()
        self.window['-WORKERS-'].update(values=self.table['-WORKERS-'])
        # self.window['-ORDERS-'].update(values=self.table['-ORDERS-'])
        # self.window['-TASKS-'].update(values=self.table['-TASKS-'])
        # self.window['-CLOSE-'].update(values=self.table['-CLOSE-'])

    # @add_logger_peewee
    def get_format_list_workers(self):
        all_workers = get_all_workers()
        self.table['-WORKERS-'] = []
        # print(f'{all_workers=}')
        if all_workers:
            for i, worker in enumerate(all_workers, start=1):
                task = worker.tasks
                # print(f'{worker=} {task=} ')
                formatted_data = (
                    i,
                    f'{worker.surname} {worker.name} {worker.second_name}',
                    str(worker.function),
                    str(task[-1].order) if task else '--',
                    task[-1].deadline if task else 0,
                    task[-1].total if task and task[-1].total else 0,
                    worker.id
                )
                self.table['-WORKERS-'].append(formatted_data)
        # print(f'{self.workers=}')

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
                task.total if task and task.total else 0,
                f'{task.master.surname} {task.master.name[:1]}.{task.master.second_name[:1]}.',
                task.status.state,
                task.id,
            ]
            formatted_data.insert(0, len(lst) + 1)
            lst.append(formatted_data)
        return lst

    # @add_logger_peewee
    def get_format_list_tasks(self):
        self.table['-TASK-M-'] = []
        self.table['-TASK-F-'] = []
        self.table['-CLOSE-'] = []
        # self.table['-TASK-M-'].extend(self._format_list_task(get_mounter_tasks()))
        # self.table['-TASK-F-'].extend(self._format_list_task(get_fitter_tasks()))
        # self.table['-CLOSE-'].extend(self._format_list_task(get_close_tasks()))
