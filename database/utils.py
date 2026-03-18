def remove_duplicate_period_date(query_list):
    d = {}
    for period in query_list:
        d[period.date] = period
    return list(d.values())
