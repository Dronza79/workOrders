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
#     tit = ['Абакумовка', 'завод ЗИЛ', 'Славянская', 'Саянская', 'Вишняковская', 'Ярино', 'Ванино', 'Разметелево']
#     type_ob = ['РУ-10кВ', 'РУ10-ЛЭП АБ', 'РУ-6кВ']
#     data_order = []
#     order = 28130
#     for i in tit:
#         for _ in range(random.randint(9, 22)):
#             obj = {}
#             order += 1
#             obj['title'] = i
#             item = 'РУ-20кВ' if i == 'завод ЗИЛ' else random.choice(type_ob)
#             obj['type_obj'] = item
#             num = (random.randint(260, 279) if item == 'РУ-6кВ'
#                    else '00' + str(random.randint(2, 9)) if item == 'РУ-20кВ' else random.randint(624, 637))
#             tunum = random.choice(['00', '03'])
#             hed = random.randint(10, 45) if tunum == '03' else '00'
#             obj['article'] = (f"ENF{'20' if item == 'РУ-20кВ' else '06' if item == 'РУ-6кВ' else '10'}"
#                               f"_{num}_{tunum}_0{hed}_00")
#             obj['article'] += '-' + str(random.randint(10, 50)) if tunum == "00" else ''
#             obj['no'] = order
#             obj['name'] = 'Отсек вторичных цепей' if tunum == '03' else 'Шкаф фидера ОМЕГА'
#             data_order.append(obj)
#
#     for i in range(0, len(data_order), 50):
#         Order.insert_many(data_order[i:i + 50]).execute()


data_task = []
with get_database().atomic():
    mechanic = Worker.select().join(Vacancy).where(Vacancy.is_fitter)  # слесяря
    mounter = Worker.select().join(Vacancy).where(Vacancy.is_mounter)
    mont_order = Order.select().where(Order.article.contains('_03_'))
    other_order = Order.select().where(~Order.article.contains('_03_'))
    m_c = mont_order.count()
    idx = 0
    for order in mont_order:
        if idx > mounter.count() - 1:
            idx = 0
        task = {
            'order': order,
            'worker': mounter[idx],
            'deadline': 42,
            'is_type': 4
        }
        idx += 1
        data_task.append(task)
    for order in other_order:
        if idx > mounter.count() - 1:
            idx = 0
        task = {
            'order': order,
            'worker': mounter[idx],
            'deadline': 42,
            'is_type': 4
        }
        idx += 1
        data_task.append(task)
        for master in mechanic:
            task = {
                'order': order,
                'worker': master,
                'deadline': 54,
                'is_type': 3
            }
            data_task.append(task)

    for i in range(0, len(data_task), 50):
        Task.insert_many(data_task[i:i + 50]).execute()


delta = datetime.timedelta(days=1)
for worker in Worker.select(Worker, Vacancy).join(Vacancy):
    date = datetime.date(2024, 8, 1)
    if worker.function.is_mounter:
        for task in worker.tasks:
            while ((date < datetime.date(2024, 11, 1)) and
                   # while ((date < datetime.date(2024, 9, 6)) and
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
    elif worker.function.is_fitter:
        for master_task in worker.tasks:
            while (date < datetime.date(2024, 11, 1)
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

# sub = Period.select(fn.SUM(Period.value)).where(Period.task == Task.id)
# query = Task.update(status=Status.select().where(Status.is_archived).get()).where(~Task.order, Task.deadline - 8 <= sub)
# query.execute()

for order in Order.select().join(Task).group_by(Order).having(peewee.fn.MAX(Task.deadline)):
    if order.tasks[-1].deadline - 8 <= sum(order.time_worked):
        print(f'{list(order.tasks)=}')
        (Task.update(status=Status.select().where(Status.is_archived).get())
         .where(Task.id.in_([task.id for task in order.tasks])).execute()
         )
