import locale
from pathlib import Path

from database.app_logger import add_logger_peewee
from database.migrations import apply_migrations
from database.settings import path
from gui.views import StartMainWindow


# @add_logger_peewee
def main():
    # print(f'{path.get_path=}')
    # print(locale.getlocale())
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
    # locale.setlocale(locale.LC_TIME, 'ru_RU')
    # print(locale.getlocale())
    if not Path(path.get_path).exists():
        apply_migrations()
    StartMainWindow()


# TODO 
#  1. Сделать возможность добавления задачи непосредственно из карточки работника и карточки ПРки. 
#  2. Реализовать настройки программы (задание должностей и статусов задач и возможность выбора функции статуса)


if __name__ == '__main__':
    main()
    
