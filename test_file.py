
import datetime

import peewee
from peewee import fn

from database.app_logger import add_logger_peewee
from database.models import Worker, Task, TypeTask, Period, Status, Vacancy, Order


@add_logger_peewee
def main():
    query = (
        Task.select(Task, Worker, Order, peewee.fn.MAX(Period.date).alias('max_date'))
        .join(Status).where(~Status.is_archived)
        .join_from(Task, Period)
        .group_by(Task))

    for i, tas in enumerate(query, start=1):
        pass

if __name__ == '__main__':
    main()
