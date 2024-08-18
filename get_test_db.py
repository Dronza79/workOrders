import random

from database.models import *

with get_database().atomic():
    FuncPosition.insert_many([[func] for func in FUNC_VARIABLES.values()], fields=['job_name']).execute()
    Status.insert_many([[value] for value in STATUS_VARIABLES.values()], ['state']).execute()
    data_person = [
        {'surname': 'Вахитов', 'name': 'Данис', 'second_name': 'Римович', 'table_num': 'A-001', 'function': 2},
        {'surname': 'Найденко', 'name': 'Георгий', 'second_name': 'Владимирович', 'table_num': 'A-002', 'function': 2},
        {'surname': 'Шмырин', 'name': 'Олег', 'second_name': 'Афанасьевич', 'table_num': 'A-003', 'function': 1},
        {'surname': 'Прокопенко', 'name': 'Юрий', 'second_name': 'Валерьевич', 'table_num': 'A-004', 'function': 2},
        {'surname': 'Полякова', 'name': 'Марина', 'second_name': 'Ивановна', 'table_num': 'A-005', 'function': 2},
        {'surname': 'Аскеров', 'name': 'Гахраман', 'second_name': 'Камаладдин Оглы', 'table_num': 'A-008',
         'function': 3},
        {'surname': 'Коробка', 'name': 'Алексей', 'second_name': 'Викторович', 'table_num': 'A-006', 'function': 4},
        {'surname': 'Пузанков', 'name': 'Максим', 'second_name': 'Витальевич', 'table_num': 'A-007', 'function': 4},
    ]
    Person.insert_many(data_person).execute()

    tit = ['Абакумовка', 'завод ЗИЛ', 'Славянская', 'Саянкая', 'Вишняковская', 'Ярино', 'Ванино', 'Разметелево']
    type_ob = ['РУ-10кВ', 'РУ10-ЛЭП АБ', 'РУ-6кВ']
    data_order = []
    order = 28130
    for i in tit:
        for _ in range(random.randint(6, 20)):
            obj = {}
            order += 1
            obj['title'] = i
            item = 'РУ-20кВ' if i == 'завод ЗИЛ' else random.choice(type_ob)
            obj['type_obj'] = item
            num = (random.randint(260, 272) if item == 'РУ-6кВ'
                   else '00' + str(random.randint(2, 8)) if item == 'РУ-20кВ'
            else random.randint(625, 637))
            tunum = random.choice(['00', '03'])
            hed = random.randint(10, 45) if tunum == '03' else '00'
            obj['article'] = (f"ENF{'20' if item == 'РУ-20кВ' else '06' if item == 'РУ-6кВ' else '10'}"
                              f"_{num}_{tunum}_0{hed}_00")
            obj['article'] += '-' + str(random.randint(10, 50)) if tunum == "00" else ''
            obj['order'] = order
            data_order.append(obj)

    ProductionOrder.insert_many(data_order).execute()

data_task = []
with get_database().atomic():
    mechanic = Person.select().where(Person.function_id.in_([3, 4]))  # слесяря
    mounter = Person.select().where(Person.function_id.in_([1, 2]))
    for order in ProductionOrder.select():
        task = {'order': order}
        if order.article[10:12] == '03':
            task['worker'] = random.choice(mounter)
            task['deadline'] = 42
            data_task.append(task)
        else:
            team = random.choice([mechanic, mounter])
            if team is mounter:
                task['worker'] = random.choice(mounter)
                task['deadline'] = 24
                data_task.append(task)
            else:
                for master in mechanic:
                    task = {
                        'order': order,
                        'worker': master,
                        'deadline': 54
                    }
                    data_task.append(task)
    for i in range(0, len(data_task), 50):
        WorkTask.insert_many(data_task[i:i + 50]).execute()

data_period = []
with get_database().atomic():
    target_date = datetime.date(2024, 1, 14)
    delta = datetime.timedelta(days=1)
    history = {}
    for _ in range(100):
        for task in (
            WorkTask.select(WorkTask, Person, ProductionOrder)
            .join_from(WorkTask, Person)
            .join_from(WorkTask, ProductionOrder)
            .group_by(WorkTask.id)
        ):
            # print(f'{task.__dict__=}')
            temp = history.setdefault(task.order, dict(deadline=task.deadline, passed=0))
            num = history.setdefault(task.worker, 0)
            # print(f'{temp=}')
            if 12 - num > 0 and temp['deadline'] - 12 >= temp['passed']:
                val = random.randint(1, 12 - num)
                period = {
                    'worker': task.worker,
                    'task': task,
                    'order': task.order,
                    'date': target_date,
                    'value': val
                }
                # print(f'{period=}')
                data_period.append(period)
                temp['passed'] += val
                history[task.worker] += val
            else:
                history[task.worker] = 0
                target_date += delta

    for i in range(0, len(data_period), 50):
        WorkPeriod.insert_many(data_period[i:i + 50]).execute()

        #
    # target_date = datetime.date(2024, 7, 11)
    # work_lapse_data = []
    # for _ in range(14):
    #     for worker in Person.select():
    #         for worker in Person.select().where(Person.function.in_([FuncPosition[3], FuncPosition[4]])):
    # if random.random() > 0.05:
    #     task = random.choice(worker.tasks.select())
    #     task = random.choice(WorkTask.select().where(WorkTask.master == worker, WorkTask.status != Status[2]))
    # duration = 8
    # duration = random.choice([8, 12])
    # print(f"{task.id}: {task}={task.deadline} =>{sum(task.time_worked)}")
    # if sum(task.time_worked) < task.deadline:
    #     laps = {'worker': worker, 'task': task, 'value': duration, 'date': target_date}
    #     WorkLapse.create(**laps)
    #     if sum(task.time_worked) >= task.deadline:
    #         task.status = Status[2]
    #         task.save()
    # target_date += datetime.timedelta(days=1)
    #
    # for task in WorkTask.select():
    #     if sum(task.time_worked) >= task.deadline:
    #         print(f"{task} {task.deadline} == {sum(task.time_worked)}")
    #         task.status = Status[2]
    #         task.save()
    #
    # query = (
    #     WorkTask.select(WorkTask, peewee.fn.SUM(WorkLapse.value).alias('total'), Person)
    #     .join_from(WorkTask, WorkLapse, peewee.JOIN.LEFT_OUTER)
    #     .join_from(WorkTask, Person)
    #     .where(WorkTask.status != Status[2], Person.function.in_([FuncPosition[3], FuncPosition[4]]))
    #     .group_by(WorkTask.order)
    # )
    #
    # for task in query:
    #     print(f"{task.id} {task} {task.deadline} == {task.total} {task.status}")
    #     if task.total >= task.deadline:
    #         print(f"{task.id}: было={task.status}", end=' ')
    #         WorkTask.update(status=Status[2]).where(WorkTask.order == task.order).execute()
    #         print(f"стало={WorkTask.select().where(WorkTask.order == task.order)[0].status}")
