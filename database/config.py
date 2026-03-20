from pathlib import Path

from peewee import SqliteDatabase

BASE_DIR = Path('.').resolve()


class DBPath:
    def __init__(self):
        self._path = BASE_DIR / f'db-current.sqlite3'

    @property
    def get_path(self):
        return self._path

    @get_path.setter
    def get_path(self, value):
        self._path = Path(value).resolve()


path = DBPath()


def get_database():
    return SqliteDatabase(path.get_path, pragmas={'foreign_keys': 1})

