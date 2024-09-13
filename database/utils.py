import re

from database.models import Worker, Vacancy, Order, Task, Status


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
            'function': 'Должность'
        }
        worker = None
        if idx:
            worker = Worker.get(Worker.id == idx)
        for key in ['surname', 'name', 'second_name', 'table_num', 'function']:
            if key != 'function':
                if key != 'second_name' and len(raw_data[key].strip()) < 3:
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
        }
        order = None
        if idx:
            order = Order.get(Order.id == idx)
        for key in ['no', 'type_obj', 'title', 'article']:
            if len(raw_data[key]) < 3:
                errors.append(f'Ошибка:\nПоле {dep[key]} не заполнено!\n')
            elif not re.findall(r'\b[А-Яа-я]+\b', raw_data[key]) and key in ['type_obj', 'title']:
                errors.append(f'Ошибка:\nПоле {dep[key]} допускаются только русские буквы!\n')
            elif key == 'article':
                if not re.findall(r'\b[A-Za-z]{3}\d{2}[_-]\d{3}[_-]\d{2}[_-]\d{3}[_-]\d{2}', raw_data[key]):
                    errors.append(f'Ошибка:\nПоле {dep[key]} заполнено не по формату!\n')
                else:
                    if (idx and getattr(order, key) != raw_data[key]) or not idx:
                        valid_data[key] = raw_data[key].upper()
            elif key == 'no':
                if not re.findall(r'\d+', raw_data[key]):
                    errors.append(f'Ошибка:\nПоле {dep[key]} заполнено не по формату!\n')
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
                    valid_data[key] = raw_data[key]

    elif entity == 'task':
        dep = {
            'order': 'Производственный заказ',
            'worker': 'Исполнитель',
            'status': 'Статус',
            'deadline': 'Норматив выполнения',
            'comment': 'Комментарии'
        }
        task = None
        if idx:
            task = Task.get(Task.id == idx)
        for key, value in {'order': Order, 'status': Status, 'worker': Worker}.items():
            print(f'{key=} {value=} {raw_data[key]=}')
            if not isinstance(raw_data[key], value) and not idx:
                errors.append(f'Ошибка:\nПоле {dep[key]} не выбрано!\n')
            else:
                if (idx and key not in ['order', 'worker'] and getattr(task, key) != raw_data[key]) or not idx:
                    valid_data[key] = raw_data[key]
        if not raw_data['deadline'].isdigit():
            errors.append(f'Ошибка:\nПоле {dep["deadline"]} допускаются только цифры!\n')
        else:
            if (idx and getattr(task, "deadline") != int(raw_data["deadline"])) or not idx:
                valid_data["deadline"] = int(raw_data["deadline"])
        if (idx and getattr(task, "comment") != raw_data["comment"]) or not idx:
            valid_data["comment"] = raw_data["comment"]

    return errors, valid_data


def validation_period_data(raw_data):
    print(f'validation_period_data {raw_data=}')