from database.models import Month
from database.queries import get_query_for_exel, get_query_for_timesheet, get_query_kpi
from database.utils import remove_duplicate_period_date
from .forms import PersonalMonthExelTable, TimeSheet


def get_personal_table_result(worker, month):
    query = get_query_for_exel(worker, month)
    print(f'{query=}')
    current_task = query.pop('current_task')
    prev_task = query.pop('prev_task')
    len_pages = len(current_task) // 6 + (1 if len(current_task) % 6 else 0)
    exel = PersonalMonthExelTable()
    target = sum(map(lambda x: x.deadline, current_task)) - sum(map(lambda x: sum(x.time_worked), prev_task))

    for idx in range(0, len(current_task) + 1, 6):
        cur_page = current_task[0 + idx:6 + idx]
        prev_data = prev_task[0 + idx:6 + idx]
        exel.fill_data(worker, month, query, target, cur_page, prev_data)
        len_pages -= 1
        if len_pages:
            exel.add_worksheet()

    return exel.save(f'{worker.surname}_{month.number:02}')


def get_month_timesheet(month: Month):
    # query = get_query_for_timesheet(month.number)
    query = get_query_for_timesheet(month)
    mean = month.get_means()
    ts = TimeSheet(month)

    sheet = 0
    ts.fill(1, 8, 'ООО ЭНЕРГОЭРА')
    ts.fill(1, 22, '  ')
    ts.fill(4, 16, month.get_lower())
    ts.fill(4, 19, f'{month.year} года')
    addr = ts.link_title
    idx = 0

    for number, worker in enumerate(query, start=1):
        over = [0, 0]
        sat = [0, 0]
        if idx + 1 > len(addr):
            sheet += 1
            addr = ts.add_other_sheet(sheet)
            idx = 0
        # print(f'{idx=} {addr=}')
        ts.fill(addr[idx], 1, number)
        data = (f'{worker.surname} {worker.name[:1]}.{f"{worker.second_name[:1]}." if worker.second_name else ""}'
                f'\n{worker.function}')
        ts.fill(addr[idx], 3, data)
        ts.fill(addr[idx], 10, worker.table_num)
        subquery = remove_duplicate_period_date(worker.time_worked)
        # first_sub = list(filter(lambda x: x.date <= mean, subquery))
        first_sub = remove_duplicate_period_date(filter(lambda x: x.date <= mean, subquery))
        # second_sub = list(filter(lambda x: x.date > mean, subquery))
        second_sub = remove_duplicate_period_date(filter(lambda x: x.date > mean, subquery))
        # print(f'{len(subquery)=} {len(first_sub)=} {len(second_sub)=}')
        ts.fill(addr[idx], 29, len(first_sub) if first_sub else '-')
        ts.fill(addr[idx] + 1, 29, sum(first_sub) if first_sub else '-')
        ts.fill(addr[idx] + 2, 29, len(second_sub) if second_sub else '-')
        ts.fill(addr[idx] + 3, 29, sum(second_sub) if second_sub else '-')
        ts.fill(addr[idx], 31, len(subquery) if subquery else '-')
        ts.fill(addr[idx] + 2, 31, sum(subquery) if subquery else '-')
        for period in subquery:
            if period.date.day > month.get_means():
                row = addr[idx] + 2
                col = period.date.day + 12 - month.get_means()
            else:
                row = addr[idx]
                col = period.date.day + 12
            ts.fill(row, col, period.sum_val)
            if period.date.weekday() == 5:
                # print(period)
                sat[0] += 1
                sat[1] += period.sum_val
            if period.sum_val > 8:
                # print(period)
                over[0] += 1
                over[1] += period.sum_val - 8
        ts.fill(addr[idx], 33, over[0] if over[0] else '-')
        ts.fill(addr[idx] + 2, 33, over[1] if over[1] else '-')
        ts.fill(addr[idx], 35, sat[0] if sat[0] else '-')
        ts.fill(addr[idx] + 2, 35, sat[1] if sat[1] else '-')
        idx += 1
    return ts.save(f'табель_{month.get_lower()}')


def get_month_kpi(month: Month):
    query = get_query_kpi(month)
    # print(query)
    filename = f'kpi-{month.number}-{month.year}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'{f"KPI {month.get_lower()} {month.year} г.":^56}\n\n\n')
        for i, worker in enumerate(query):
            kpi = 0
            if worker.total_fact:
                kpi = worker.total_plan / worker.total_fact
            file.write(
                f" {i + 1}. {worker.get_short_name()}\t\t| План: {worker.total_plan}\t"
                f"| Факт: {worker.total_fact}\t| KPI: {kpi:.2f}\n\n")

    return filename
