import re
from datetime import datetime as dt

from database.models import Worker, Vacancy, Order, Task, Status, Period, TypeTask


def validation_data(raw_data, idx=None):
    errors = []
    valid_data = {}
    entity = raw_data.get('type')
    if entity == 'worker':
        dep = {
            'surname': 'Фамилия',
            'name': 'Имя',
            'table_num': 'Табельный номер',
            'second_name': 'Отчество',
            'function': 'Должность',
            'ordinal': 'Порядковой номер'
        }
        worker = None
        if idx:
            worker = Worker.get(Worker.id == idx)
            print(f'{worker.__data__=}')
        for key in ['surname', 'name', 'second_name', 'table_num', 'function', 'ordinal']:
            if key != 'function':
                if key not in ['second_name', 'ordinal'] and len(raw_data[key].strip()) < 3:
                    errors.append(f'Ошибка:\nПоле {dep[key]} не заполнено! (мин. 3 буквы)\n')
                elif key in ['surname', 'name'] or (key == 'second_name' and raw_data['second_name'].strip()):
                    if not re.findall(r'\b[А-Яа-я]+\b', raw_data[key].strip()):
                        errors.append(f'Ошибка:\nПоле {dep[key]} допускаются только русские буквы!\n')
                    else:
                        if (idx and getattr(worker, key).lower() != raw_data[key].strip().lower()) or not idx:
                            valid_data[key] = raw_data[key].strip().capitalize()
                elif key == 'table_num':
                    if not idx or getattr(worker, key) != raw_data[key].strip():
                        if Worker.get_or_none(Worker.table_num == raw_data[key].strip().capitalize()):
                            errors.append(f'Ошибка:\nРаботник с таким Табельным номером уже существует!\n')
                        else:
                            if (idx and getattr(worker, key).lower() != raw_data[key].strip().lower()) or not idx:
                                valid_data[key] = raw_data[key].strip().capitalize()
                elif key == 'ordinal':
                    if not worker or getattr(worker, key) != raw_data[key].strip():
                        valid_data[key] = raw_data[key].strip()
            else:
                if not isinstance(raw_data[key], Vacancy):
                    errors.append(f'Ошибка:\nПоле {dep[key]} не выбрано!\n')
                else:
                    if (idx and getattr(worker, key) != raw_data[key]) or not idx:
                        valid_data[key] = raw_data[key]

    elif entity == 'order':
        dep = {
            'no': 'Номер производственного заказа',
            'type_obj': 'Тип объекта',
            'title': 'Наименование объекта',
            'article': 'Конструктив',
            'name': 'Название заказа',
        }
        order = None
        if idx:
            order = Order.get(Order.id == idx)
            if raw_data['name'] and raw_data['name'] != order.name:
                valid_data['name'] = raw_data['name']
        if not idx and raw_data['name']:
            valid_data['name'] = raw_data['name']
        for key in ['no', 'type_obj', 'title', 'article']:
            if len(raw_data[key]) < 3:
                errors.append(f'Ошибка:\nПоле {dep[key]} не заполнено!\n')
            elif key in ['type_obj', 'title'] and not re.findall(r'\b[^A-z]+\b', raw_data[key]):
                errors.append(f'Ошибка:\nПоле {dep[key]} допускаются только русские буквы!\n')
            elif key == 'article':
                if not re.findall(r'\b[^А-я]+\b', raw_data[key]):
                # if not re.findall(r'\b[A-Za-z]{3}\d{2}[_-]\d{3}[_-]\d{2}[_-]\d{3}[_-]\d{2}', raw_data[key]):
                    errors.append(f'Ошибка:\nПоле {dep[key]} допускается только латиница!\n')
                else:
                    if (idx and getattr(order, key) != raw_data[key]) or not idx:
                        valid_data[key] = raw_data[key].strip().upper()
            elif key == 'no':
                if not re.findall(r'\d+', raw_data[key]):
                    errors.append(f'Ошибка:\nПоле {dep[key]} допускаются только цифры!\n')
                elif not idx or order.to_order != raw_data['no']:
                    # print('Проверка номера=', Order.get_or_none(Order.no == int(re.findall(r'\d+', raw_data['no']).pop())))
                    if Order.get_or_none(Order.no == int(re.findall(r'\d+', raw_data['no']).pop())):
                        errors.append(f'Ошибка:\nЗаказ с таким номером уже существует!\n')
                    else:
                        if (idx and getattr(order, key) != raw_data[key]) or not idx:
                            # print('получение номера=', int(re.findall(r'\d+', raw_data[key]).pop()))
                            valid_data[key] = int(re.findall(r'\d+', raw_data[key]).pop())
            else:
                if (idx and getattr(order, key) != raw_data[key]) or not idx:
                    valid_data[key] = raw_data[key].strip()

    elif entity == 'task':
        dep = {
            'is_type': 'Тип задачи',
            'order': 'Производственный заказ',
            'worker': 'Исполнитель',
            'status': 'Статус',
            'deadline': 'Норматив выполнения',
            'comment': 'Комментарии'
        }
        task = None
        if idx:
            task = Task.get_by_id(idx)
        for key, value in {'order': Order, 'status': Status, 'worker': Worker, 'is_type': TypeTask}.items():
            # print(f'{key=} {value=} {raw_data[key]=}')
            if idx:
                if key == 'status' and task.status != raw_data[key]:
                    valid_data[key] = raw_data[key]
            else:
                if not isinstance(raw_data[key], value) and key != 'order':
                    errors.append(f'Ошибка:\nПоле {dep[key]} не выбрано!\n')
                elif key == 'order':
                    if isinstance(raw_data[key], value):
                        valid_data[key] = raw_data[key]
                else:
                    valid_data[key] = raw_data[key]

        print(f'{valid_data=}')
        if not raw_data['deadline'].isdigit():
            errors.append(f'Ошибка:\nПоле {dep["deadline"]} допускаются только цифры!\n')
        else:
            if (idx and getattr(task, "deadline") != int(raw_data["deadline"])) or not idx:
                valid_data["deadline"] = int(raw_data["deadline"])
        if (idx and getattr(task, "comment") != raw_data["comment"]) or not idx:
            valid_data["comment"] = raw_data["comment"]

    return errors, valid_data


def validation_period_data(raw_data, idx=None):
    # print(f'validation_period_data {raw_data=}')
    valid_data = {}
    errors = []
    date = raw_data.get('date')
    period = None
    task = raw_data.get('task')
    if idx:
        period = Period[int(idx)]
        valid_data['period_id'] = raw_data['period_id']
    else:
        valid_data['worker'] = task.worker
        valid_data['task'] = task
        valid_data['order'] = task.order
    if re.findall(r'\b\d{2}\.\d{2}\.\d{4}\b', date):
        if (idx and getattr(period, 'date') != dt.strptime(date, '%d.%m.%Y').date()) or not idx:
            valid_data['date'] = dt.strptime(date, '%d.%m.%Y').date()
    else:
        errors.append('Ошибка.\nДата указана не верно!\nВоспользуйтесь кнопкой Календарь!')
    if idx:
        if raw_data.get('value') != getattr(period, 'value'):
            valid_data['value'] = raw_data.get('value')
    else:
        if list(Period.select().where(Period.task == task, Period.date == valid_data['date'])):
            errors.append('Ошибка.\nПериод с такой датой уже существует!\nИзмените существующий!')
        else:
            valid_data['value'] = raw_data.get('value')

    # print(f'{errors=} {valid_data=}')
    return errors, valid_data


def validation_data_for_exel(raw_data):
    print(f'{raw_data=}')
    valid_data = {}
    errors = []
    if not isinstance(raw_data['-worker-'], Worker):
        errors.append('Ошибка.\nВы не выбрали работника)!')
    else:
        valid_data['worker'] = raw_data['-worker-']
    valid_data['month'] = raw_data['-month-']

    return errors, valid_data


def remove_duplicate_period_date(query_list):
    d = {}
    for period in query_list:
        d[period.date] = period
    return list(d.values())
