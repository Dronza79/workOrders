import re

from database.models import Worker, Vacancy, Order


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
            worker = Worker.select().where(Worker.id == idx).dicts().get()
        for key in ['surname', 'name', 'second_name', 'table_num', 'function']:
            if key not in ['second_name', 'function'] and len(raw_data[key]) < 3:
                errors.append(f'Ошибка:\nПоле {dep[key]} не заполнено! (мин. 3 буквы)\n')
            elif key in ['surname', 'name'] or (key == 'second_name' and raw_data['second_name']):
                if not re.findall(r'\b[А-Яа-я]+\b', raw_data[key]):
                    errors.append(f'Ошибка:\nПоле {dep[key]} допускаются только русские буквы!\n')
            if key == 'table_num':
                if not idx or worker['table_num'] != raw_data['table_num']:
                    if Worker.get_or_none(Worker.table_num == raw_data['table_num']):
                        errors.append(f'Ошибка:\nРаботник с таким Табельным номером уже существует!\n')
            if key == 'function' and not isinstance(raw_data[key], Vacancy):
                errors.append(f'Ошибка:\nПоле {dep[key]} не выбрано!\n')
            if not idx:
                valid_data[key] = raw_data[key]
            else:
                if key != 'function' and worker[key].capitalize() != raw_data[key].capitalize():
                    valid_data[key] = raw_data[key]
                elif key == 'function' and raw_data[key].id != worker[key]:
                    valid_data[key] = raw_data[key]
            if key in ['surname', 'name', 'second_name']:
                if valid_data.get(key):
                    valid_data[key] = valid_data[key].capitalize()
    elif entity == 'order':
        dep = {
            'no': 'Номер производственного заказа',
            'type_obj': 'Тип объекта',
            'title': 'Наименование объекта',
            'article': 'Конструктив',
        }
        order = None
        if idx:
            order = Order.select().where(Order.id == idx).get()
            # order = Order.select().where(Order.id == idx).dicts().get()
            print(f'{order=}')
        for key in ['no', 'type_obj', 'title', 'article']:
            if len(raw_data[key]) < 3:
                errors.append(f'Ошибка:\nПоле {dep[key]} не заполнено!\n')
            elif key == 'article' and not re.findall(
                    r'\b[A-Z]{3}\d{2}[_-]\d{3}[_-]\d{2}[_-]\d{3}[_-]\d{2}', raw_data[key]):
                errors.append(f'Ошибка:\nПоле {dep[key]} заполнено не по формату!\n')
            elif key == 'no':
                print(f'{idx=}')
                if not idx or order.to_order != raw_data['no']:
                    if Order.get_or_none(Order.no == int(re.findall(r'\d+', raw_data['no']).pop())):
                        errors.append(f'Ошибка:\nЗаказ с таким номером уже существует!\n')

    return errors, valid_data
