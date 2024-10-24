import locale
from datetime import datetime

import peewee
from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from peewee import fn

from database.app_logger import add_logger_peewee
from database.models import Worker, Task, TypeTask, Period, Status, Vacancy, Order, Month
from database.settings import get_database


@add_logger_peewee
def main():
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
    ws: Worksheet = Workbook().active
    month = Month(9)
    start, mean, end = month.get_border_dates()
    print(f'{start=}\n{mean=}\n{end=}')
    w = Worker.select(Worker, Vacancy).join(Vacancy).order_by(Worker.surname, Worker.name, Worker.second_name)
    p = (
        Period.select(
            Period,
            peewee.fn.SUM(Period.value).over(partition_by=[Period.worker, Period.date]).alias('sum_val'))
        .where(Period.date >= start, Period.date <= end).order_by(Period.date))
    query = peewee.prefetch(w, p)

    for i, worker in enumerate(query):
        print(f'{worker.surname} отработал всего={sum(worker.time_worked)}')
        print(f'1 половина={sum(filter(lambda x: x.date <= mean, worker.time_worked))}')
        print(f'2 половина={sum(filter(lambda x: x.date > mean, worker.time_worked))}')
        idx = 4
        for period in worker.time_worked:
            day = period.date.day
            if day <= 15:
                col = 12 + day
                row = 9 + idx * i
            else:
                col = day - 3
                row = 9 + 2 + idx * i
            cell: Cell = ws.cell(row, col)
            print(f'ячейка({cell.coordinate}) = {period} {period.sum_val}')
        print()


if __name__ == '__main__':
    main()
