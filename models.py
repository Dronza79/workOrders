import datetime
import re

from peewee import *

from .settings import get_database


STATUS_VARIABLES = [
    {'state': 'В работе', },
    {'state': 'Приостановлен', 'is_positive': False},
    {'state': 'Завершен', 'is_archived': True},
]

TYPE_VARIABLES = [
    {'title': 'Погрузо-разгрузочная работа', 'has_extension': False},
    {'title': 'Подсобная работа', 'has_extension': False},
    {'title': 'Сборочная работа', 'has_extension': True},
    {'title': 'Монтажная работа', 'has_extension': True},
]

FUNC_VARIABLES = [
    {'post': 'Старший монтажник', 'is_slave': False, 'is_mounter': True},
    {'post': 'Монтажник', 'is_mounter': True},
    {'post': 'Старший слесарь', 'is_slave': False, 'is_fitter': True},
    {'post': 'Слесарь', 'is_fitter': True},
]


class BaseModel(Model):
    create_at = DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания')
    update_at = DateTimeField(default=datetime.datetime.now, verbose_name='Дата изменения')
    is_active = BooleanField(verbose_name='Отслеживается', default=True)

    class Meta:
        database = get_database()
        only_save_dirty = True

    def save(self, **kwargs):
        self.update_at = datetime.datetime.now()
        super().save(**kwargs)


class Vacancy(BaseModel):
    post = CharField(verbose_name='Должность')
    is_slave = BooleanField(default=True, verbose_name='Подчиненый')  # подчиненый
    is_staff = BooleanField(default=False, verbose_name='Персонал')  # персонал
    is_mounter = BooleanField(default=False, verbose_name='Монтажник')  # монтажник
    is_fitter = BooleanField(default=False, verbose_name='Сборщик')  # слесарь
    is_checked = BooleanField(default=False, verbose_name='Приемка')  # приемка
    is_store = BooleanField(default=False, verbose_name='Склад')  # склад

    def __str__(self):
        return self.post


class Worker(BaseModel):
    surname = CharField(verbose_name='Фамилия', constraints=[Check('surname != ""')])
    name = CharField(verbose_name='Имя', constraints=[Check('name != ""')])
    second_name = CharField(verbose_name='Отчество', default='')
    table_num = CharField(unique=True, verbose_name='Табельный номер', constraints=[Check('table_num != ""')])
    function = ForeignKeyField(Vacancy, verbose_name='Должность', on_delete='CASCADE')

    def __str__(self):
        return (
            f'{self.surname} '
            f'{self.name[:1]}.'
            f'{self.second_name[:1]+"." if self.second_name else ""} ({self.function.post})')


class Status(BaseModel):
    state = CharField(verbose_name='Наименование')
    is_positive = BooleanField(default=True)
    is_archived = BooleanField(default=False)

    def __str__(self):
        return self.state


class Order(BaseModel):
    no = SmallIntegerField(unique=True, index=True, verbose_name='ПРка')
    type_obj = CharField(verbose_name='Тип объекта')
    title = CharField(verbose_name='Наименование объекта')
    article = CharField(verbose_name='Конструктив')
    name = CharField(verbose_name='Наименование заказа', null=True)

    def __str__(self):
        num = 6 - len(str(self.no))
        return f'ПР-{"0" * num}{self.no}'

    @property
    def to_order(self):
        return self.__str__()

    @to_order.setter
    def to_order(self, string_order):
        self.no = int(re.findall(r'\d+', string_order).pop())


class TypeTask(BaseModel):
    title = CharField(verbose_name='Наименование типа')
    has_extension = BooleanField(verbose_name='Предусмотрена ПРка')

    def __str__(self):
        return self.title


class Task(BaseModel):
    is_type = ForeignKeyField(TypeTask, backref='tasks', verbose_name='Тип задачи', on_delete='CASCADE')
    order = ForeignKeyField(Order, backref='tasks', verbose_name='Заказ', on_delete='CASCADE', null=True)
    worker = ForeignKeyField(Worker, backref='tasks', verbose_name='Работник', on_delete='CASCADE')
    status = ForeignKeyField(Status, backref='tasks', verbose_name='Состояние', default=1, on_delete='CASCADE')
    deadline = SmallIntegerField(verbose_name='Норматив выполнения')
    comment = TextField(verbose_name='Комментарий', default='')

    # def __str__(self):
    #     return f'{self.id} ({self.status.state})'


class Period(BaseModel):
    worker = ForeignKeyField(Worker, verbose_name='Работник', backref='time_worked', on_delete='CASCADE')
    task = ForeignKeyField(Task, backref='time_worked', verbose_name='Задача', on_delete='CASCADE')
    order = ForeignKeyField(Order, backref='time_worked', null=True, verbose_name='Задача', on_delete='CASCADE')
    date = DateField(default=datetime.datetime.now, verbose_name='Дата')
    value = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'id:{self.id} {self.date:%d.%m.%y} ({self.date:%a}) - {self.value} ч.'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.value + other.value) if isinstance(other, self.__class__) else (
            int(self.value + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.value) if isinstance(other, (int, float)) else NotImplemented

    def get_day_week(self):
        return f'{self.date:%a}', int(f'{self.date:%w}')
# import peewee
# from database.models import Task, Period, Status, Worker, Order
# for i, task in enumerate(Task.select(), start=1):
#     print(i, task.id)

# tasks = Task.select(Task, Period, peewee.fn.SUM(Period.value).alias('passed')).join_from(Task, Period, peewee.JOIN.LEFT_OUTER).group_by(Task.id)