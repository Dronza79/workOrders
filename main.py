import locale
import os
import platform
from pathlib import Path

from database.app_logger import add_logger_peewee
from database.migrations import apply_migrations
from database.settings import path
from gui.views import StartMainWindow


@add_logger_peewee
def main():
    # print(f'{path.get_path=}')
    # print(locale.getlocale())
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
    # locale.setlocale(locale.LC_TIME, 'ru_RU')
    if not Path(path.get_path).exists():
        apply_migrations()
    with open('log.txt', 'a+', encoding='utf8') as file:
        system = platform.system()  # Название ОС
        release = platform.release()  # Версия ОС
        version = platform.version()  # Полная версия ОС
        architecture = platform.architecture()
        user = os.getlogin()
        file.write(f'{user=}\n{system=}\n{release=}\n'
                   f'{version=}\n{architecture=}\n{"*" * 30}\n')
    StartMainWindow()


# TODO 
# 1.	Добавить модель "Тип задачи" +
# 2.	Номер Ордера сделать строкой -
# 3.	Сделать возможность добавления задачи непосредственно из карточки работника и карточки ПРки. +
# 4.	Реализовать настройки программы (задание должностей и статусов задач и возможность выбора функции статуса)
# 5.	Оперативная информация за текущий месяц
# 6.	Добавить фильтр ПРок в карточку задач +
# 7.	Добавить тип задачи "Погрузо-разгрузочные работы", "Подсобные работы" +
# 8.	Получить информацию о проработанных работником часах за конкретный день
# 9.	Вывод количества отработанных часов за указанный период по всем работникам
# 10.	Добавить конфиги к моделям "Статус", "Должность", «Тип задачи» +



if __name__ == '__main__':
    main()


# import datetime
#
# import peewee
#
# from database.app_logger import add_logger_peewee
# from database.models import Worker, Task, TypeTask, Period, Status, Vacancy, Order
#
#
# @add_logger_peewee
# def main():
#     now_date = datetime.date(2024, 9, 1)
#     query = (
#         # Worker.select(Worker, Vacancy, Task, TypeTask, Period, Status, Order)
#         Worker.select(
#             Worker.id.alias('worker_id'), Task.id.alias('task_id'), Order.id.alias('order_id'),
#             Period.id.alias('period_id'), Worker.surname, Vacancy.post, TypeTask.title, Status.state,
#             Order.no, Period.date, Period.value)
#         .join_from(Worker, Vacancy)
#         .join_from(Worker, Task, peewee.JOIN.LEFT_OUTER)
#         .join_from(Task, TypeTask)
#         .join_from(Task, Order, peewee.JOIN.LEFT_OUTER)
#         .join_from(Task, Status)
#         .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
#         # .join_from(Worker, Period, peewee.JOIN.LEFT_OUTER)
#         .where(~Status.is_archived)
#         .order_by(Worker, -Period.date)
#         .group_by(Worker.id)
#         # .having(Period.date.year == now_date.year, Period.date.month == now_date.month)
#         .dicts())
#     for i, worker in enumerate(query, start=1):
#         print(f'{i}. {worker}')
#
#
# if __name__ == '__main__':
#     main()
