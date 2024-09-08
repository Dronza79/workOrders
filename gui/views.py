from datetime import datetime
from operator import itemgetter

import PySimpleGUI as sg

from database.queries import (
    get_all_workers,
    get_open_tasks,
    get_close_tasks,
    get_worker_data,
    get_task_data,
    get_all_orders, create_new_period
)
from .components import get_card_worker, get_card_task
from .windows import get_main_window, get_card_window, popup_get_period


class StartWindowCard:
    def __init__(self, parent, raw_data=None, key=None, ):
        self.idx = raw_data[-1] if raw_data else None
        self.key = key
        self.parent = parent
        self.window = get_card_window(form=self.key)
        self.run()

    def run(self):
        card = []
        if self.key == '-WRK-':
            data = get_worker_data(idx=self.idx)
            card = get_card_worker(data)
        elif self.key in ['-CLS-', '-TSK-']:
            data = get_task_data(idx=self.idx)
            card = get_card_task(data)
        elif self.key == '-ORD-':
            data = get_order_data(idx=self.idx)
            card = get_card_order(data)
        self.window.extend_layout(self.window['body'], card)
        self.move_center()
        while True:
            ev, val = self.window.read()
            print(f'{ev=} {val=}')
            if ev in [sg.WIN_CLOSED, '-CANCEL-']:
                break
            elif ev == 'order':
                order = val.get(ev)
                self.window['type_obj'].update(order.type_obj)
                self.window['title'].update(order.title)
                self.window['article'].update(order.article)
                self.window.refresh()
            elif ev == '-ADD-TIME-':
                period = popup_get_period(self.window)
                if period:
                    tsk = get_task_data(val.get('task')).get('task').get()
                    data = {
                        'worker': tsk.worker,
                        'task': tsk,
                        'order': tsk.order,
                        'date': datetime.strptime(period.get('date'), '%d.%m.%Y'),
                        'value': period.get('value')
                    }
                    create_new_period(data)
                    new_data = get_task_data(val.get('task'))
                    time_worked = '\n'.join([str(period) for period in new_data.get('time_worked', [])])
                    self.window['-PASSED-'].update(new_data.get('task').get().passed)
                    self.window['-TIME-WORKED-'].update(time_worked)
                    self.window.refresh()
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
            elif ev in ['-WORKERS-', '-ORDERS-', '-TASKS-', '-CLOSE-', '-ADD-']:
                # print(f"{val.get(ev)=}")
                # print(f"{self.table.get(ev)=} {val.get(ev)=}")
                kwargs = {
                    'raw_data': self.table[ev][val[ev].pop()] if val.get(ev) else None,
                    'key': val.get('-TG-'),
                    'parent': self.window
                }
                # print(f'{kwargs=}')
                StartWindowCard(**kwargs)
                self.actualizing()

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
        self.get_format_list_orders()
        self.get_format_list_tasks()
        self.window['-WORKERS-'].update(values=self.table['-WORKERS-'])
        self.window['-ORDERS-'].update(values=self.table['-ORDERS-'])
        self.window['-TASKS-'].update(values=self.table['-TASKS-'])
        self.window['-CLOSE-'].update(values=self.table['-CLOSE-'])

    def get_format_list_workers(self):
        all_workers = get_all_workers()
        self.table['-WORKERS-'] = []
        if all_workers:
            for i, worker in enumerate(all_workers, start=1):
                period = worker.time_worked
                if period:
                    period = period[-1]
                    total_worked = period.task.total_time
                    # print(f'{worker=} {period=} {total_worked=}')
                else:
                    period = None
                    total_worked = None
                formatted_data = (
                    i,
                    f'{worker.surname} {worker.name} {worker.second_name}',
                    str(worker.function),
                    str(period.order) if period else '--',
                    period.task.deadline if period else 0,
                    total_worked if total_worked else 0,
                    worker.id
                )
                self.table['-WORKERS-'].append(formatted_data)
        # print(f'{self.workers=}')

    def get_format_list_orders(self):
        all_orders = get_all_orders()
        self.table['-ORDERS-'] = []
        if all_orders:
            for i, order in enumerate(all_orders, start=1):
                tasks = order.tasks
                if tasks:
                    worker = tasks[0].worker
                else:
                    worker = None
                formatted_data = (
                    i,
                    str(order),
                    order.type_obj,
                    order.title,
                    order.article,
                    f'{worker.surname} {worker.name[:1]}.{worker.second_name[:1]}.' if worker else '---',
                    order.order
                )
                # print(f'{formatted_data=}')

                self.table['-ORDERS-'].append(formatted_data)

    @staticmethod
    def _format_list_task(list_task):
        if not list_task:
            return []
        lst = []
        for i, task in enumerate(list_task, start=1):
            formatted_data = [
                i,
                str(task.order),
                task.deadline,
                task.total_worked,
                f'{task.worker.surname} {task.worker.name[:1]}.{task.worker.second_name[:1]}.',
                str(task.status),
                task.id,
            ]
            # formatted_data.insert(0, len(lst) + 1)
            lst.append(formatted_data)
        return lst

    def get_format_list_tasks(self):
        self.table['-TASKS-'] = []
        self.table['-CLOSE-'] = []
        self.table['-TASKS-'].extend(self._format_list_task(get_open_tasks()))
        self.table['-CLOSE-'].extend(self._format_list_task(get_close_tasks()))
