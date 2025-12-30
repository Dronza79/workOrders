import locale
import os
import platform
from datetime import datetime
from pathlib import Path

from database.app_logger import add_logger_peewee
from database.migrations import apply_migrations, migrations_v1_1_0, get_program_setting
from database.models import ProgramSetting
from database.settings import path
from gui.views import StartMainWindow


# @add_logger_peewee
def main():
    # print(f'{path.get_path=}')
    # print(locale.getlocale())
    locale.setlocale(locale.LC_ALL, '')
    if not Path(path.get_path).exists():
        apply_migrations()
    ver: ProgramSetting = get_program_setting()
    if ver.patch != 2:
        ver.patch = 2
        ver.save()

    StartMainWindow()


# TODO 
# 1.	Добавить настройки предзаполнения эксель таблиц (Ответственный, руководитель, организация подразделение)
# 2.	Добавить возможность заведения своих должностей
# 3.    Добавить авторизацию по логину и паролю
# 4.    Добавить порядковый номер каждому работнику. Внести изменение без замены БД


if __name__ == '__main__':
    main()
