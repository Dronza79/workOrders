import os
from operator import itemgetter

import PySimpleGUI as sg

from database.queries import (
    get_all_workers, get_open_tasks,
    get_close_tasks, get_worker_data,
    get_task_data, get_all_orders,
    create_new_period, get_order_data,
    create_or_update_entity, get_all_dismiss,
    get_period, update_delete_period,
    delete_or_restore
)
from database.utils import validation_data, validation_period_data
from tablesExcel.processor import get_personal_table_result
from .components import (
    get_card_worker, get_card_task,
    get_card_order, get_list_task_for_worker,
    get_list_task_for_order
)
from .templates_settings import error_popup_setting, info_popup_setting
from .windows import (
    get_main_window, get_card_window,
    popup_get_period, popup_choice_worker_for_exel,
    popup_find_string
)


class StartWindowCard:
    value = None
    old_data = None

    def __init__(self, parent, idx=None, key=None, prefill=None):
        self.idx = int(idx) if idx else None
        self.key = key
        self.parent = parent
        self.window = get_card_window(form=self.key)
        self.windows_extend(prefill)
        self.run()

    def run(self):
        while True:
            ev, self.value = self.window.read()
            ev = ev if isinstance(ev, tuple) or ev == sg.WIN_CLOSED else ev.split(sg.MENU_KEY_SEPARATOR)[-1]
            print(f'WindowCard {ev=} {self.value=}')
            if ev in [sg.WIN_CLOSED, '-CANCEL-', 'Escape:27']:
                break
            elif ev in ['order', 'worker']:
                search = self.value.get(ev)
                if isinstance(search, str):
                    self.old_data = self.window[ev].Values
                    new_data = list(filter(lambda obj: search.lower() in str(obj).lower(), self.old_data))
                    self.window[ev].update(new_data[0], values=new_data)
                elif ev == 'order':
                    self.window['type_obj'].update(search.type_obj)
                    self.window['title'].update(search.title)
                    self.window['article'].update(search.article)
                    self.window['-PASSED-'].update(search.passed)
                else:
                    self.window[ev].update(self.value[ev], values=self.old_data)
            elif ev == '-ADD-TIME-':
                button, period_data = popup_get_period(self.window)
                if button == '-SAVE-PER-' and period_data:
                    period_data.update(get_task_data(self.value.get('id')))
                    errors, valid_data = validation_period_data(period_data)
                    if errors:
                        sg.popup('\n'.join(errors), title='Ошибка', location=self.get_location(), **error_popup_setting)
                    else:
                        if create_new_period(valid_data):
                            sg.popup_timed('Сохранено', location=self.get_location(), **info_popup_setting)
                            self.actualizing_passed_period()
            elif ev == '-TIME-WORKED-':
                period = get_period(idx=self.window[ev].Values[self.value.get(ev)[0]][-1])
                ev_per, val_per = popup_get_period(self.window, period)
                # print(f'Period {ev_per=} {val_per=} {self.value.get("id")=}')
                if ev_per in ['-SAVE-PER-', '-DEL-PER-']:
                    errors, valid_data = validation_period_data(val_per, val_per.get('period_id'))
                    if errors:
                        sg.popup('\n'.join(errors), title='Ошибка', location=self.get_location(), **error_popup_setting)
                    else:
                        if update_delete_period(valid_data, ev_per):
                            sg.popup_timed('Сохранено', location=self.get_location(), **info_popup_setting)
                            self.actualizing_passed_period()
                        else:
                            sg.popup_timed('Изменения не вносились!', location=self.get_location(), **info_popup_setting)
            elif ev in ['-DOUBLE-TASKS-', '-ADD-TASK-']:
                if self.value['type'] == 'worker':
                    entity = get_worker_data(int(self.value.get('id'))).get('tasks')
                    list_comprehension = get_list_task_for_worker
                else:
                    entity = get_order_data(int(self.value.get('id'))).get('tasks')
                    list_comprehension = get_list_task_for_order
                if ev == '-ADD-TASK-':
                    idx = None
                    choice = self.value['type']
                    prefill = (
                        choice,
                        self.value['id'],
                    )
                else:
                    idx = entity[self.value[ev].pop()].id
                    prefill = None
                self.window.hide()
                StartWindowCard(
                    idx=idx,
                    key='-TSK-',
                    parent=self.window,
                    prefill=prefill
                )
                self.window.un_hide()
                self.window.force_focus()
                if self.value['type'] == 'worker':
                    entity = get_worker_data(int(self.value.get('id'))).get('tasks')
                else:
                    entity = get_order_data(int(self.value.get('id'))).get('tasks')
                self.window['-DOUBLE-TASKS-'].update(list(list_comprehension(entity)))
                # self.window.refresh()
            elif ev == '-SAVE-':
                errors, valid_data = validation_data(self.value, self.idx)
                if errors:
                    sg.popup('\n'.join(errors), title='Ошибка', location=self.get_location(), **error_popup_setting)
                else:
                    if valid_data:
                        result = create_or_update_entity(key=self.value.get('type'), data=valid_data, idx=self.idx)
                        if result:
                            sg.popup_timed('Сохранено', location=self.get_location(), **info_popup_setting)
                            break
                    else:
                        sg.popup_timed('Изменения не вносились', location=self.get_location(), **info_popup_setting)
            elif ev in ['-DELETE-', '-RESTORE-']:
                res = delete_or_restore(self.value.get('type'), int(self.value.get('id')))
                if res:
                    sg.popup_timed('Сохранено', location=self.get_location(), **info_popup_setting)
                    break
            elif ev == 'is_type':
                types = self.value[ev]
                if types.has_extension:
                    self.window['-ORDER-TASK-'].update(visible=True)
                else:
                    self.window['-ORDER-TASK-'].update(visible=False)
                    self.window['-PASSED-'].update(0)
                    self.window.refresh()
            elif ev == '-FIND-':
                if search := popup_find_string(self.window):
                    self.filter_list(search)
        self.window.close()

    def get_location(self):
        self.window.refresh()
        size_w, size_h = self.window.current_size_accurate()
        loc_x, loc_y = self.window.current_location()
        return loc_x + size_w // 2 - 150, loc_y + size_h // 2 - 20

    def move_center(self):
        size_w, size_h = self.parent.current_size_accurate()
        loc_x, loc_y = self.parent.current_location()
        self.window.refresh()
        size = self.window.current_size_accurate()
        self.window.move(loc_x + size_w // 2 - size[0] // 2, loc_y + size_h // 2 - size[1] // 2)
        # self.window.move(*self.get_location())

    def windows_extend(self, prefill):
        card = []
        if self.key in ['-WRK-', '-DSMS-']:
            data = get_worker_data(idx=self.idx)
            card = get_card_worker(data)
        elif self.key in ['-CLS-', '-TSK-']:
            data = get_task_data(idx=self.idx)
            card = get_card_task(data, prefill)
        elif self.key == '-ORD-':
            data = get_order_data(idx=self.idx)
            card = get_card_order(data)
        self.window.extend_layout(self.window['body'], [card])
        self.move_center()

    def filter_list(self, find):
        def func(string):
            return any(map(lambda x: find.lower() in str(x).lower(), string))

        new_data = list(filter(func, self.window['-DOUBLE-TASKS-'].Values))
        self.window['-DOUBLE-TASKS-'].update(values=new_data)

    def actualizing_passed_period(self):
        data = get_task_data(self.value.get('id'))
        print(f'{data=}')
        time_worked = [
            [
                f'{period.date if period else "":%d.%m.%y}',
                f'{period.date if period else "":%a}',
                f'{period.value if period else ""} ч.',
            ] for period in data.get('time_worked', [])]
        passed = data.get('passed_order') if data.get('passed_order') else data.get('passed_task')
        self.window['-PASSED-'].update(passed)
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
    mapping = {
        '-WRK-': '-WORKERS-',
        '-DSMS-': '-DISMISS-',
        '-TSK-': '-TASKS-',
        '-CLS-': '-CLOSE-',
        '-ORD-': '-ORDERS-'
    }
    sort = False
    sort_col = None

    def __init__(self):
        self.window = get_main_window()
        self.window.maximize()
        self.actualizing()
        self.run()

    def run(self):
        while True:
            ev, val = self.window.read()
            ev = ev if isinstance(ev, tuple) or ev == sg.WIN_CLOSED else ev.split(sg.MENU_KEY_SEPARATOR)[-1]
            print(f'MainWindow {ev=} {val=}')
            if ev == sg.WIN_CLOSED:
                break
            elif ev in ['-TG-', '-UPDATE-', 'Escape:27']:
                self.actualizing()
            elif isinstance(ev, tuple) and ev[2][0] == -1:
                self.sorting_list(ev[0], ev[2][1])
            elif ev in ['-WORKERS-', '-ORDERS-', '-TASKS-', '-CLOSE-', '-ADD-', '-DISMISS-']:
                # self.window.alpha_channel = .95
                StartWindowCard(
                    idx=self.table[ev][val[ev].pop()][-1] if val.get(ev) else None,
                    key=val.get('-TG-'),
                    parent=self.window)
                # self.window.alpha_channel = 1
                self.actualizing()
            elif ev == '-THEME-':
                if sg.main_global_pysimplegui_settings():
                    self.window.close()
                    StartMainWindow()
            elif ev == '-EXEL-':
                valid_data = popup_choice_worker_for_exel(self.window)
                # popup_output()
                if file_path := get_personal_table_result(**valid_data):
                    sg.popup_timed('Исполнено', **info_popup_setting)
                    os.startfile(file_path, 'open')

            elif ev in ['-FIND-', '??:70', 'f:70']:
                key_table = self.mapping.get(val.get('-TG-'))
                if search := popup_find_string(self.window):
                    self.filter_list(key_table, search)
            self.window.force_focus()
        self.window.close()

    def sorting_list(self, key_table, column):
        if column == self.sort_col:
            self.sort = not self.sort
        else:
            self.sort = False
        self.sort_col = column
        self.table[key_table] = sorted(self.table[key_table], key=itemgetter(column), reverse=self.sort)
        self.window[key_table].update(values=self.table[key_table])

    def filter_list(self, key_table, find):
        # print(f'filter_list({key_table=}, {find=})')

        def func(string):
            return any(map(lambda x: find.lower() in str(x).lower(), string))

        self.table[key_table] = list(filter(func, self.table[key_table]))
        self.window[key_table].update(values=self.table[key_table])

    def actualizing(self):
        self.get_format_list_workers()
        self.get_format_list_orders()
        self.get_format_list_tasks()
        [self.window[key].update(values=self.table[key]) for key in self.table]

    @staticmethod
    def _format_list_workers(lst_workers):
        if not lst_workers:
            return []
        lst = []
        dash = '--'
        for i, worker in enumerate(lst_workers, start=1):
            formatted_data = (
                i,
                f'{worker.surname} {worker.name} {worker.second_name}',
                worker.table_num,
                worker.post,
                worker.type_task if worker.type_task else dash,
                f'ПР-{worker.order_num:06}' if worker.order_num else dash,
                worker.dltask if worker.dltask else dash,
                worker.sum_period if worker.sum_period else dash,
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
                formatted_data = (
                    i,
                    str(order),
                    order.type_obj,
                    order.title,
                    order.article,
                    order.name if order.name else '--',
                    order.deadline if order.deadline else '--',
                    order.passed if order.passed else '--',
                    f'{tasks[-1].status}' if tasks else '---',
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
                str(task.is_type),
                str(task.status),
                f'{task.worker.surname} {task.worker.name[:1]}.{task.worker.second_name[:1]}.',
                task.deadline,
                task.passed if task.passed else 0,
                str(task.order) if task.order else '--',
                task.order.type_obj if task.order else '--',
                task.order.title if task.order else '--',
                task.order.name if task.order and task.order.name else '--',
                task.id,
            ]
            lst.append(formatted_data)
        return lst

    def get_format_list_tasks(self):
        self.table['-TASKS-'] = []
        self.table['-CLOSE-'] = []
        self.table['-TASKS-'].extend(self._format_list_task(get_open_tasks()))
        self.table['-CLOSE-'].extend(self._format_list_task(get_close_tasks()))
