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


class Vacancy(BaseModel):
    post = CharField(verbose_name='Должность')

    def __str__(self):
        return self.post


class Worker(BaseModel):
    surname = CharField(verbose_name='Фамилия')
    name = CharField(verbose_name='Имя')
    second_name = CharField(null=True, verbose_name='Отчество')
    table_num = CharField(unique=True, verbose_name='Табельный номер')
    function = ForeignKeyField(Vacancy, verbose_name='Должность', on_delete='CASCADE')
    is_active = BooleanField(verbose_name='Отслеживается', default=True)

    def __str__(self):
        return f'{self.surname} {self.name[:1]}.{self.second_name[:1]}. ({self.function.post})'


class Status(BaseModel):
    state = CharField(verbose_name='Наименование')

    def __str__(self):
        return self.state


class Order(BaseModel):
    order = SmallIntegerField(primary_key=True, unique=True, index=True, verbose_name='ПРка')
    type_obj = CharField(verbose_name='Тип объекта')
    title = CharField(verbose_name='Наименование объекта')
    article = CharField(verbose_name='Конструктив')

    def __str__(self):
        num = 6 - len(str(self.order))
        return f'ПР-{"0" * num}{self.order}'


class Task(BaseModel):
    order = ForeignKeyField(Order, backref='tasks', verbose_name='Заказ', on_delete='CASCADE')
    worker = ForeignKeyField(Worker, backref='tasks', verbose_name='Работник', on_delete='CASCADE')
    status = ForeignKeyField(Status, backref='tasks', verbose_name='Состояние', default=1, on_delete='CASCADE')
    deadline = SmallIntegerField(verbose_name='Норматив выполнения')
    comment = TextField(verbose_name='Комментарий', default='')

    def __str__(self):
        return f'{self.order} ({self.status.state})'


class Period(BaseModel):
    worker = ForeignKeyField(Worker, verbose_name='Работник', backref='time_worked', on_delete='CASCADE')
    task = ForeignKeyField(Task, backref='time_worked', verbose_name='Задача', on_delete='CASCADE')
    order = ForeignKeyField(Order, backref='time_worked', verbose_name='Задача', on_delete='CASCADE')
    date = DateField(default=datetime.datetime.now, verbose_name='Дата')
    value = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'{self.value} ч. ({self.date:%d-%m-%Y})'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.value + other.value) if isinstance(other, self.__class__) else (
            int(self.value + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.value) if isinstance(other, (int, float)) else NotImplemented

    def get_day_week(self):
        return f'{self.date:%a}', int(f'{self.date:%w}')
