import random

import peewee

from database.models import *

with get_database().atomic():
    FuncPosition.insert_many([[func] for func in FUNC_VARIABLES.values()], fields=['job_name']).execute()
    Status.insert_many([[value] for value in STATUS_VARIABLES.values()], ['state']).execute()
    data_person = [
        {'surname': 'Вахитов', 'name': 'Данис', 'second_name': 'Римович', 'table_num': '1', 'function': 2},
        {'surname': 'Найденко', 'name': 'Георгий', 'second_name': 'Владимирович', 'table_num': '2', 'function': 2},
        {'surname': 'Шмырин', 'name': 'Олег', 'second_name': 'Афанасьевич', 'table_num': '3', 'function': 1},
        {'surname': 'Прокопенко', 'name': 'Юрий', 'second_name': 'Валерьевич', 'table_num': '4', 'function': 2},
        {'surname': 'Полякова', 'name': 'Мирина', 'second_name': 'Ивановна', 'table_num': '5', 'function': 2},
        {'surname': 'Аскеров', 'name': 'Гахраман', 'second_name': 'Камаладдин Оглы', 'table_num': '8', 'function': 3},
        {'surname': 'Коробка', 'name': 'Алексей', 'second_name': 'Викторович', 'table_num': '6', 'function': 4},
        {'surname': 'Пузанков', 'name': 'Максим', 'second_name': 'Витальевич', 'table_num': '7', 'function': 4},
    ]
    Person.insert_many(data_person).execute()
    data_task = [
        {'type_obj': 'Ру-10кВ', 'title': 'Ярино', 'article': 'ENF10_637_03_044_00', 'order': 'ПР-028108', 'deadline': 42, 'master': 1},
        {'type_obj': 'Ру-10кВ ЛЭП АБ', 'title': 'Ярино', 'article': 'ENF10_633_03_065_00', 'order': 'ПР-028208', 'deadline': 42, 'master': 2},
        {'type_obj': 'Ру-10кВ', 'title': 'Абакумовка', 'article': 'ENF10_633_03_065_00', 'order': 'ПР-028258', 'deadline': 42, 'master': 3},
        {'type_obj': 'Ру-10кВ ЛЭП АБ', 'title': 'Ярино', 'article': 'ENF10_633_03_065_00', 'order': 'ПР-028278', 'deadline': 42, 'master': 4},
        {'type_obj': 'Ру-20кВ', 'title': 'ЗИЛ', 'article': 'ENF20_003_00_000_00-03', 'order': 'ПР-028103', 'deadline': 24, 'master': 5},
        {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_003_00_000_00-03', 'order': 'ПР-028203', 'deadline': 24, 'master': 1},
        {'type_obj': 'Ру-10кВ', 'title': 'Саянская', 'article': 'ENF10_634_03_022_00', 'order': 'ПР-027111', 'deadline': 42, 'master': 2},
        {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_635_00_000_00-03', 'order': 'ПР-028643', 'deadline': 24, 'master': 3},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028104', 'deadline': 24, 'master': 4},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_633_03_067_00', 'order': 'ПР-028113', 'deadline': 42, 'master': 5},
        {'type_obj': 'Ру-10кВ', 'title': 'Саянская', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028313', 'deadline': 54, 'master': 6},
        {'type_obj': 'Ру-10кВ', 'title': 'Саянская', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028313', 'deadline': 54, 'master': 7},
        {'type_obj': 'Ру-10кВ', 'title': 'Саянская', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028313', 'deadline': 54, 'master': 8},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028314', 'deadline': 54, 'master': 6},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028314', 'deadline': 54, 'master': 7},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028314', 'deadline': 54, 'master': 8},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028315', 'deadline': 54, 'master': 6},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028315', 'deadline': 54, 'master': 7},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028315', 'deadline': 54, 'master': 8},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028316', 'deadline': 54, 'master': 6},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028316', 'deadline': 54, 'master': 7},
        {'type_obj': 'Ру-10кВ', 'title': 'Ванино', 'article': 'ENF10_629_00_000_00-18', 'order': 'ПР-028316', 'deadline': 54, 'master': 8},
        {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028317', 'deadline': 54, 'master': 6},
        {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028317', 'deadline': 54, 'master': 7},
        {'type_obj': 'Ру-10кВ', 'title': 'Саларьево', 'article': 'ENF10_633_00_000_00-67', 'order': 'ПР-028317', 'deadline': 54, 'master': 8},
    ]
    WorkTask.insert_many(data_task).execute()

target_date = datetime.date(2024, 7, 11)
work_lapse_data = []
for _ in range(14):
    for worker in Person.select():
    # for worker in Person.select().where(Person.function.in_([FuncPosition[3], FuncPosition[4]])):
        if random.random() > 0.05:
            task = random.choice(worker.tasks.select())
            # task = random.choice(WorkTask.select().where(WorkTask.master == worker, WorkTask.status != Status[2]))
            duration = 8
            # duration = random.choice([8, 12])
            print(f"{task.id}: {task}={task.deadline} =>{sum(task.time_worked)}")
            if sum(task.time_worked) < task.deadline:
                laps = {'worker': worker, 'task': task, 'value': duration, 'date': target_date}
                WorkLapse.create(**laps)
                if sum(task.time_worked) >= task.deadline:
                    task.status = Status[2]
                    task.save()
    target_date += datetime.timedelta(days=1)


# for task in WorkTask.select():
#     if sum(task.time_worked) >= task.deadline:
#         print(f"{task} {task.deadline} == {sum(task.time_worked)}")
#         task.status = Status[2]
#         task.save()

query = (
    WorkTask.select(WorkTask, peewee.fn.SUM(WorkLapse.value).alias('total'), Person)
    .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
    .join_from(WorkTask, Person)
    .where(WorkTask.status != Status[2], Person.function.in_([FuncPosition[3], FuncPosition[4]]))
    .group_by(WorkTask.order)
)

for task in query:
    print(f"{task.id} {task} {task.deadline} == {task.total} {task.status}")
    if task.total >= task.deadline:
        print(f"{task.id}: было={task.status}", end=' ')
        WorkTask.update(status=Status[2]).where(WorkTask.order == task.order).execute()
        print(f"стало={WorkTask.select().where(WorkTask.order == task.order)[0].status}")

