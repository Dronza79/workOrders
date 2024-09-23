import random

import peewee

from database.models import *

# with get_database().atomic():
#     # Vacancy.insert_many([[func] for func in FUNC_VARIABLES.values()], fields=['post']).execute()
#     # Status.insert_many([[value] for value in STATUS_VARIABLES.values()], ['state']).execute()
#     data_person = [
#         {'surname': 'Вахитов', 'name': 'Данис', 'second_name': 'Римович', 'table_num': 'A-001', 'function': 2},
#         {'surname': 'Найденко', 'name': 'Георгий', 'second_name': 'Владимирович', 'table_num': 'A-002', 'function': 2},
#         {'surname': 'Шмырин', 'name': 'Олег', 'second_name': 'Афанасьевич', 'table_num': 'A-003', 'function': 1},
#         {'surname': 'Прокопенко', 'name': 'Юрий', 'second_name': 'Валерьевич', 'table_num': 'A-004', 'function': 2},
#         {'surname': 'Полякова', 'name': 'Марина', 'second_name': 'Ивановна', 'table_num': 'A-005', 'function': 2},
#         {'surname': 'Аскеров', 'name': 'Гахраман', 'second_name': 'Камаладдин Оглы', 'table_num': 'A-008',
#          'function': 3},
#         {'surname': 'Коробка', 'name': 'Алексей', 'second_name': 'Викторович', 'table_num': 'A-006', 'function': 4},
#         {'surname': 'Пузанков', 'name': 'Максим', 'second_name': 'Витальевич', 'table_num': 'A-007', 'function': 4},
#     ]
#     Worker.insert_many(data_person).execute()
#
#     tit = ['Абакумовка', 'завод ЗИЛ', 'Славянская', 'Саянкая', 'Вишняковская', 'Ярино', 'Ванино', 'Разметелево']
#     type_ob = ['РУ-10кВ', 'РУ10-ЛЭП АБ', 'РУ-6кВ']
#     data_order = []
#     order = 28130
#     for i in tit:
#         for _ in range(random.randint(5, 10)):
#             obj = {}
#             order += 1
#             obj['title'] = i
#             item = 'РУ-20кВ' if i == 'завод ЗИЛ' else random.choice(type_ob)
#             obj['type_obj'] = item
#             num = (random.randint(260, 279) if item == 'РУ-6кВ'
#                    else '00' + str(random.randint(2, 9)) if item == 'РУ-20кВ'
#             else random.randint(624, 637))
#             tunum = random.choice(['00', '03'])
#             hed = random.randint(10, 45) if tunum == '03' else '00'
#             obj['article'] = (f"ENF{'20' if item == 'РУ-20кВ' else '06' if item == 'РУ-6кВ' else '10'}"
#                               f"_{num}_{tunum}_0{hed}_00")
#             obj['article'] += '-' + str(random.randint(10, 50)) if tunum == "00" else ''
#             obj['no'] = order
#             data_order.append(obj)
#
#     Order.insert_many(data_order).execute()
#
# data_task = []
# with get_database().atomic():
#     mechanic = Worker.select().where(Worker.function_id.in_([3, 4]))  # слесяря
#     mounter = Worker.select().where(Worker.function_id.in_([1, 2]))
#     for order in Order.select():
#         task = {'order': order}
#         if order.article[10:12] == '03':
#             task['worker'] = random.choice(mounter)
#             task['deadline'] = 42
#             data_task.append(task)
#         else:
#             team = random.choice([mechanic, mounter])
#             if team is mounter:
#                 task['worker'] = random.choice(mounter)
#                 task['deadline'] = 24
#                 data_task.append(task)
#             else:
#                 for master in mechanic:
#                     task = {
#                         'order': order,
#                         'worker': master,
#                         'deadline': 54
#                     }
#                     data_task.append(task)
#     for i in range(0, len(data_task), 50):
#         Task.insert_many(data_task[i:i + 50]).execute()
#
# # data_period = []
# # with get_database().atomic():
# #     target_date = datetime.date(2024, 1, 14)
# #     delta = datetime.timedelta(days=1)
# #     history = {}
# #     for _ in range(30):
# #         for task in (
# #             Task.select(Task, Worker, Order)
# #             .join_from(Task, Worker)
# #             .join_from(Task, Order)
# #             .group_by(Task.id)
# #         ):
# #             # print(f'{task.__dict__=}')
# #             temp = history.setdefault(task.order, dict(deadline=task.deadline, passed=0))
# #             num = history.setdefault(task.worker, 0)
# #             # print(f'{temp=}')
# #             if 12 - num > 0 and temp['deadline'] - 12 >= temp['passed']:
# #                 val = random.randint(1, 12 - num)
# #                 period = {
# #                     'worker': task.worker,
# #                     'task': task,
# #                     'order': task.order,
# #                     'date': target_date,
# #                     'value': val
# #                 }
# #                 # print(f'{period=}')
# #                 data_period.append(period)
# #                 temp['passed'] += val
# #                 history[task.worker] += val
# #             else:
# #                 history[task.worker] = 0
# #                 target_date += delta
# #
# #     for i in range(0, len(data_period), 50):
# #         Period.insert_many(data_period[i:i + 50]).execute()
#
# # sub = Period.select(fn.SUM(Period.value)).where(Period.task == Task.id)
# # query = Task.update(status_id=2).where(Task.deadline - 8 < sub)
# # query.execute()

query = (
    Worker.select(Worker, Task, Order, Period)
    .join_from(Worker, Task, peewee.JOIN.LEFT_OUTER)
    .join_from(Task, Period, peewee.JOIN.LEFT_OUTER)
    .join_from(Task, Order)
    .group_by(Worker)
)
delta = datetime.timedelta(days=1)
print(list(query))
for worker in query:
    date = datetime.date(2024, 8, 1)
    if worker.function_id < 3:
        for task in worker.tasks:
            while ((date < datetime.date(2024, 9, 6)) and
                   (sum(task.time_worked) < task.deadline - 8)):
                if date.isoweekday() != 7:
                    per = Period.create(
                        worker=worker,
                        task=task,
                        order=task.order,
                        date=date,
                        value=8 if date.isoweekday() not in [2, 4] else 12
                    )
                    print(per)
                date += delta
    elif worker.function_id == 3:
        for master_task in worker.tasks:
            while (date < datetime.date(2024, 9, 6)
                   and (sum(master_task.order.time_worked) < (master_task.deadline - 8))):
                if date.isoweekday() != 7:
                    for task in master_task.order.tasks:
                        per = Period.create(
                            worker=task.worker,
                            task=task,
                            order=task.order,
                            date=date,
                            value=8 if date.isoweekday() not in [2, 4] else 12
                        )
                        print(per)
                date += delta
