import datetime
import importlib
import os
import sqlite3 as sql
from pathlib import Path

from database.settings import path, get_database


# def create_dump_db():
#     """
#     создание дампа для MySQL из БД SQLite3
#     :return:
#     """
#     db = sql.connect(path.get_path)
#     time = datetime.datetime.now()
#     basename = '-'.join([Path(path.get_path).resolve().stem, str(time.date()), str(time.time())])
#     basename = basename.replace(':', '-').replace('.', '-')
#     dumpname = f'dump-{basename}.sql'
#     with open(dumpname, 'w', encoding='utf-8') as file:
#         for line in db.iterdump():
#             line = line.replace('"', '`'
#                                 ).replace('INTEGER', 'INT').replace('BEGIN', 'START')
#
#             file.write(line + '\n')
#     db.close()
#     return dumpname


def create_dump_db(path_folder='.'):
    """
    Создание дампа БД для SQLite3
    :return:
    """
    db = sql.connect(path.get_path)
    time = datetime.datetime.now()
    basename = '-'.join([Path(path.get_path).resolve().stem, str(time.date()), str(time.time())])
    basename = basename.replace(':', '-').replace('.', '-')
    base_dir = Path(path_folder).resolve()
    dumpname = base_dir / f'dump-{basename}.sql'
    with db:
        with open(dumpname, 'w', encoding='utf-8') as file:
            for line in db.iterdump():
                file.write(line + '\n')

    return dumpname


def restore_from_dump(dump_file):
    db = get_database()
    db.drop_tables(importlib.import_module('database.models').models)
    with open(dump_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    with db.connection_context():
        db.execute_sql('PRAGMA foreign_keys = OFF;')
        db.connection().executescript(sql_script)
        db.execute_sql('PRAGMA foreign_keys = ON;')
