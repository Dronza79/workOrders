from pathlib import Path

from database.migrations import apply_migrations
from database.utils import path
from gui.views import StartMainWindow


def main():
    # print(f'{path.get_path=}')
    if not Path(path.get_path).exists():
        apply_migrations()
    main_window = StartMainWindow()
    main_window.run()


if __name__ == '__main__':
    main()
    