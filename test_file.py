import locale
from datetime import datetime

import peewee
from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from peewee import fn

from database.app_logger import add_logger_peewee
from database.models import Worker, Task, TypeTask, Period, Status, Vacancy, Order, Month
from database.queries import get_query_for_timesheet
from database.settings import get_database


@add_logger_peewee
def main():
    locale.setlocale(locale.LC_ALL, '')
    ws: Worksheet = Workbook().active
    month = Month(9)
    start, mean, end = month.get_border_dates()
    query = get_query_for_timesheet(month.number)

    for i, worker in enumerate(query):
        subquery = worker.time_worked
        print(f'{worker.surname} отработал всего={sum(worker.time_worked)}')
        print(f'1 половина={sum(filter(lambda x: x.date <= mean, subquery))}')
        print(f'2 половина={sum(filter(lambda x: x.date > mean, subquery))}')
        idx = 4
        for period in subquery:
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
