import re

from database.models import Worker, Vacancy


def validation_data(raw_data):
    errors = []
    valid_data = raw_data.copy()
    entity = valid_data.pop('type')
    if entity == 'worker':
        dep = {
            'surname': 'Фамилия',
            'name': 'Имя',
            'table_num': 'Табельный номер',
            'second_name': 'Отчество',
            'function': 'Должность'
        }
        for key in valid_data:
            if key not in ['second_name', 'function'] and len(valid_data[key]) < 3:
                errors.append(f'Ошибка:\nПоле {dep[key]} не заполнено! (мин. 3 буквы)\n')
            elif key in ['surname', 'name'] or (key == 'second_name' and valid_data['second_name']):
                if not re.findall(r'\b[А-Яа-я]+\b', valid_data[key]):
                    errors.append(f'Ошибка:\nПоле {dep[key]} допускаются только русские буквы!\n')
            if key == 'table_num':
                if Worker.get_or_none(Worker.table_num == valid_data['table_num']):
                    errors.append(f'Ошибка:\nРаботник с таким Табельным номером уже существует!\n')
            if key == 'function' and not isinstance(valid_data[key], Vacancy):
                print(f'{isinstance(valid_data[key], Vacancy)=}')
                errors.append(f'Ошибка:\nПоле {dep[key]} не выбрано!\n')
            if key in ['surname', 'name', 'second_name']:
                valid_data[key] = valid_data[key].capitalize()

    return errors, valid_data
