import locale
import os
import platform
from datetime import datetime
from pathlib import Path

from database.app_logger import add_logger_peewee
from database.migrations import apply_migrations
from database.settings import path
from gui.views import StartMainWindow


# @add_logger_peewee
def main():
    # print(f'{path.get_path=}')
    # print(locale.getlocale())
    locale.setlocale(locale.LC_ALL, '')
    if not Path(path.get_path).exists():
        apply_migrations()
    with open('log.txt', 'a+', encoding='utf8') as file:
        system = platform.system()  # Название ОС
        release = platform.release()  # Версия ОС
        version = platform.version()  # Полная версия ОС
        architecture = platform.architecture()
        user = os.getlogin()
        file.write(f'{datetime.now()}\n{user=}\n{system=}\n{release=}\n'
                   f'{version=}\n{architecture=}\nlocale={locale.getlocale()}\n{"*" * 30}\n')
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
