import datetime

from peewee import *

from .utils import get_database


STATUS_VARIABLES = {
    1: 'В работе',
    2: 'Завершен',
    3: 'Приостановлен',
}

FUNC_VARIABLES = {
    1: 'Старший монтажник',
    2: 'Монтажник',
    3: 'Старший слесарь',
    4: 'Слесарь',
}


class BaseModel(Model):
    create_at = DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания')
    update_at = DateTimeField(default=datetime.datetime.now, verbose_name='Дата изменения')

    class Meta:
        database = get_database()
        only_save_dirty = True

    def save(self, **kwargs):
        self.update_at = datetime.datetime.now()
        super().save(**kwargs)


class FuncPosition(BaseModel):
    job_name = CharField(verbose_name='Должность')

    def __str__(self):
        return self.job_name


class Person(BaseModel):
    surname = CharField(verbose_name='Фамилия')
    name = CharField(verbose_name='Имя')
    second_name = CharField(null=True, verbose_name='Отчество')
    table_num = CharField(unique=True, verbose_name='Табельный номер')
    function = ForeignKeyField(FuncPosition, verbose_name='Должность', on_delete='CASCADE')

    def __str__(self):
        return f'{self.surname} {self.name[:1]}.{self.second_name[:1]}. ({self.function.job_name})'


class Status(BaseModel):
    state = CharField(verbose_name='Наименование')

    def __str__(self):
        return self.state


class WorkTask(BaseModel):
    type_obj = CharField(verbose_name='Тип объекта')
    title = CharField(verbose_name='Наименование объекта')
    article = CharField(verbose_name='Конструктив')
    order = CharField(verbose_name='Производственный заказ')
    deadline = SmallIntegerField(verbose_name='Норматив выполнения')
    master = ForeignKeyField(Person, backref='tasks', verbose_name='Работник', on_delete='CASCADE')
    status = ForeignKeyField(Status, backref='tasks', verbose_name='Состояние', default=1, on_delete='CASCADE')
    comment = TextField(verbose_name='Комментарий', null=True)

    def __str__(self):
        return self.order


class WorkLapse(BaseModel):
    worker = ForeignKeyField(Person, verbose_name='Работник', backref='time_worked', on_delete='CASCADE')
    task = ForeignKeyField(WorkTask, backref='time_worked', verbose_name='Задача', on_delete='CASCADE')
    date = DateField(default=datetime.datetime.now, verbose_name='Дата')
    value = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'{self.value} ч. ({self.date:%d-%m-%Y})'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.value + other.value) if isinstance(other, self.__class__) else (
            int(self.value + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.value) if isinstance(other, (int, float)) else NotImplemented


class Turn(BaseModel):
    worker = ForeignKeyField(Person, verbose_name='Работник', backref='turns', on_delete='CASCADE')
    date = DateField(verbose_name='Дата', default=datetime.datetime.now)
    value = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'{self.value} ч.'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.value + other.value) if isinstance(other, self.__class__) else (
            int(self.value + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.value) if isinstance(other, (int, float)) else NotImplemented





                    # work_lapse_data.append(laps)
    # for i in range(0, len(work_lapse_data), 50):
    #     WorkLapse.insert_many(work_lapse_data[i:i + 50]).execute()



# tasks = WorkTask.select(WorkTask.id, WorkTask.order, WorkTask.duration, fn.SUM(WorkLapse.term).alias('total')).join(WorkLapse, JOIN.LEFT_OUTER).group_by(WorkTask.id).dicts()
# tasks = WorkTask.select(WorkTask, Status).join(Status)
# laps = WorkLapse.select()
# result = prefetch(tasks, laps)
#
# ts = WorkTask.select(WorkTask.order, WorkTask.duration, WorkTask.time_worked, fn.SUM(WorkTask.time_worked).alias('summ'))
