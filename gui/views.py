from datetime import datetime
from operator import itemgetter

import PySimpleGUI as sg

from database.queries import (
    get_all_workers,
    get_open_tasks,
    get_close_tasks,
    get_worker_data,
    get_task_data,
    get_all_orders, create_new_period, get_order_data, create_or_update_entity, get_all_dismiss,
    delete_or_restore_worker, get_period, update_delete_period
)
from database.utils import validation_data, validation_period_data
from .components import get_card_worker, get_card_task, get_card_order, get_list_task_for_worker, \
    get_list_task_for_order
from .templates_settings import error_popup_setting
from .windows import get_main_window, get_card_window, popup_get_period


class StartWindowCard:
    value = None

    def __init__(self, parent, raw_data=None, key=None):
        self.idx = int(raw_data[-1]) if raw_data else None
        self.key = key
        self.parent = parent
        self.window = get_card_window(form=self.key)
        self.windows_extend()
        print(f'{raw_data=} {key=} {self.idx=}')
        self.run()

    def run(self):
        while True:
            ev, self.value = self.window.read()
            print(f'WindowCard {ev=} {self.value=}')
            if ev in [sg.WIN_CLOSED, '-CANCEL-']:
                break
            elif ev == 'order':
                order = self.value.get(ev)
                self.window['type_obj'].update(order.type_obj)
                self.window['title'].update(order.title)
                self.window['article'].update(order.article)
                self.window.refresh()
            elif ev == '-ADD-TIME-':
                _, period_data = popup_get_period(self.window)
                if period_data:
                    # tsk = get_task_data(self.value.get('task')).get('task').get()
                    period_data.update(get_task_data(self.value.get('task')))
                    errors, valid_data = validation_period_data(period_data)
                    if errors:
                        sg.popup('\n'.join(errors), title='Ошибка', **error_popup_setting)
                    else:
                        if create_new_period(valid_data):
                            sg.popup('Запись сохранена', title='Информация', **error_popup_setting)
                            self.actualizing_passed_period()
            elif ev == '-TIME-WORKED-':
                period = get_period(pos=self.value.get(ev)[0], task=self.value.get('task'))
                ev_per, val_per = popup_get_period(self.window, period)
                print(f'Period {ev_per=} {val_per=} {self.value.get("task")=}')
                if ev_per in ['-SAVE-PER-', '-DEL-PER-']:
                    errors, valid_data = validation_period_data(val_per, val_per.get('period_id'))
                    if errors:
                        sg.popup('\n'.join(errors), title='Ошибка', **error_popup_setting)
                    else:
                        if update_delete_period(valid_data, ev_per):
                            sg.popup('Изменения сохранены', title='Информация', **error_popup_setting)
                            self.actualizing_passed_period()
                        else:
                            sg.popup('Изменения не вносились!', title='Информация', **error_popup_setting)

            elif ev == '-DOUBLE-TASKS-':
                if self.value['type'] == 'worker':
                    entity = get_worker_data(int(self.value.get('worker_id'))).get('tasks')
                    list_comprehension = get_list_task_for_worker
                else:
                    entity = get_order_data(int(self.value.get('order_id'))).get('tasks')
                    list_comprehension = get_list_task_for_order
                StartWindowCard(
                    raw_data=['', entity[self.value[ev].pop()].id],
                    key='-TSK-',
                    parent=self.window
                )
                if self.value['type'] == 'worker':
                    entity = get_worker_data(int(self.value.get('worker_id'))).get('tasks')
                else:
                    entity = get_order_data(int(self.value.get('order_id'))).get('tasks')
                self.window['-DOUBLE-TASKS-'].update(list(list_comprehension(entity)))
                self.window.refresh()
            elif ev == '-SAVE-':
                errors, valid_data = validation_data(self.value, self.idx)
                if errors:
                    sg.popup('\n'.join(errors), **error_popup_setting)
                else:
                    if valid_data:
                        result = create_or_update_entity(key=self.value.get('type'), data=valid_data, idx=self.idx)
                        if result:
                            sg.popup('Запись сохранена', title='Ошибка', **error_popup_setting)
                            break
                    else:
                        sg.popup('Изменения не вносились', title='Информация', **error_popup_setting)
            elif ev in ['-DELETE-', '-RESTORE-']:
                res = delete_or_restore_worker(int(self.value.get('worker_id')))
                if res:
                    sg.popup('Запись сохранена', title='Информация', **error_popup_setting)
                    break
        self.window.close()

    def move_center(self):
        size_w, size_h = self.parent.current_size_accurate()
        loc_x, loc_y = self.parent.current_location()
        self.window.refresh()
        size = self.window.current_size_accurate()
        self.window.move(loc_x + size_w // 2 - size[0] // 2, loc_y + size_h // 2 - size[1] // 2)

    def windows_extend(self):
        card = []
        w, h = self.window.current_size_accurate()
        if self.key in ['-WRK-', '-DSMS-']:
            data = get_worker_data(idx=self.idx)
            card = get_card_worker(data)
            if not self.idx:
                self.window.size = (w, h - 270)
        elif self.key in ['-CLS-', '-TSK-']:
            data = get_task_data(idx=self.idx)
            card = get_card_task(data)
            if not self.idx:
                self.window.size = (w, h - 190)
        elif self.key == '-ORD-':
            data = get_order_data(idx=self.idx)
            card = get_card_order(data)
            if self.idx:
                self.window.size = (w, h - 110)
            else:
                self.window.size = (w, h - 360)
        self.window.extend_layout(self.window['body'], card)
        self.move_center()

    def actualizing_passed_period(self):
        data = get_task_data(self.value.get('task'))
        time_worked = [
            [
                f'{period.date if period else "":%d.%m.%y}',
                f'{period.date if period else "":%a}',
                f'{period.value if period else ""} ч.',
            ] for period in data.get('time_worked', [])]
        self.window['-PASSED-'].update(data.get('passed'))
        self.window['-TIME-WORKED-'].update(time_worked)
        self.window.refresh()


class StartMainWindow:
    table = {
        '-WORKERS-': [],
        '-ORDERS-': [],
        '-TASKS-': [],
        '-CLOSE-': [],
        '-DISMISS-': [],
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
            print(f'MainWindow {ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            elif ev in ['-TG-', '-UPDATE-']:
                self.actualizing()
            elif isinstance(ev, tuple) and ev[2][0] == -1:
                self.sorting_list(ev[0], ev[2][1])
            elif ev in ['-WORKERS-', '-ORDERS-', '-TASKS-', '-CLOSE-', '-ADD-', '-DISMISS-']:
                StartWindowCard(
                    raw_data=self.table[ev][val[ev].pop()] if val.get(ev) else None,
                    key=val.get('-TG-'),
                    parent=self.window
                )
                self.actualizing()

        self.window.close()

    def sorting_list(self, key_table, column):
        if self.sort_col == column:
            self.sort = not self.sort
        self.table[key_table] = sorted(self.table[key_table], key=itemgetter(column), reverse=self.sort)
        self.window[key_table].update(values=self.table[key_table])
        if self.sort_col == column:
            self.sort = not self.sort
        self.sort_col = column

    def actualizing(self):
        self.get_format_list_workers()
        self.get_format_list_orders()
        self.get_format_list_tasks()
        self.window['-WORKERS-'].update(values=self.table['-WORKERS-'])
        self.window['-ORDERS-'].update(values=self.table['-ORDERS-'])
        self.window['-TASKS-'].update(values=self.table['-TASKS-'])
        self.window['-CLOSE-'].update(values=self.table['-CLOSE-'])
        self.window['-DISMISS-'].update(values=self.table['-DISMISS-'])

    @staticmethod
    def _format_list_workers(lst_workers):
        if not lst_workers:
            return []
        lst = []
        for i, worker in enumerate(lst_workers, start=1):
            period = worker.time_worked
            if period:
                period = period[-1]
                total_worked = period.task.total_time
            else:
                period = None
                total_worked = None
            formatted_data = (
                i,
                f'{worker.surname} {worker.name} {worker.second_name}',
                worker.table_num,
                str(worker.function),
                str(period.order) if period else '--',
                period.task.deadline if period else 0,
                total_worked if total_worked else 0,
                worker.id
            )
            lst.append(formatted_data)
        return lst

    def get_format_list_workers(self):
        self.table['-WORKERS-'] = []
        self.table['-DISMISS-'] = []
        self.table['-WORKERS-'].extend(self._format_list_workers(get_all_workers()))
        self.table['-DISMISS-'].extend(self._format_list_workers(get_all_dismiss()))

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
                    order.id
                )

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
            lst.append(formatted_data)
        return lst

    def get_format_list_tasks(self):
        self.table['-TASKS-'] = []
        self.table['-CLOSE-'] = []
        self.table['-TASKS-'].extend(self._format_list_task(get_open_tasks()))
        self.table['-CLOSE-'].extend(self._format_list_task(get_close_tasks()))
