from pathlib import Path

from database.app_logger import add_logger_peewee
from database.migrations import apply_migrations
from database.utils import path
from gui.views import StartMainWindow


@add_logger_peewee
def main():
    # print(f'{path.get_path=}')
    if not Path(path.get_path).exists():
        apply_migrations()
    StartMainWindow()


if __name__ == '__main__':
    main()
    