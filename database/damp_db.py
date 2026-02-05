import datetime
import sqlite3 as sql
from pathlib import Path

from database.settings import path


def create_dump_db():

    db = sql.connect(path.get_path)
    time = datetime.datetime.now()
    basename = '-'.join([Path(path.get_path).resolve().stem, str(time.date()), str(time.time())])
    basename = basename.replace(':', '-').replace('.', '-')
    dumpname = f'dump-{basename}.sql'
    with open(dumpname, 'w', encoding='utf-8') as file:
        for line in db.iterdump():
            line = line.replace('"', '`'
                                ).replace('INTEGER', 'INT').replace('BEGIN', 'START')

            file.write(line + '\n')
    db.close()
    return dumpname

