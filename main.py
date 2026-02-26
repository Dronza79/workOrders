import importlib
import locale
from pathlib import Path

from database.app_logger import add_logger_peewee
from database.migrations import apply_migrations, get_program_setting, migrations_v2_0_0
from database.models import ProgramSetting
from database.settings import path
from gui.views import StartMainWindow


# @add_logger_peewee
def main():
    sg = importlib.import_module('PySimpleGUI')
    locale.setlocale(locale.LC_ALL, '')
    if not Path(path.get_path).exists():
        apply_migrations()
    migrations_v2_0_0()
    setting: ProgramSetting = get_program_setting()
    setting.version = '1.6.0'
    if not setting.theme:
        setting.theme = 'Default1'
    sg.theme(setting.theme)
    StartMainWindow()


# TODO 
# [*]    Выбор года вывода данных в таблицу
# [*]    Добавить вывод таблицы KPI (Ключевые показатели эффективности)
# [*]    ДОбавить переключение на другой файл базы данных, создание дампа для MySQL
# [*]    Откорректировать список работников (исключить уволенных)
# []	Добавить настройки предзаполнения эксель таблиц (Ответственный, руководитель, организация подразделение)
# []	Добавить возможность заведения своих должностей
# []    Добавить авторизацию по логину и паролю
# []    ДОбавить возможность выбирать несколько ПРок в в выполняемую задачу



if __name__ == '__main__':
    main()
