import calendar
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
    {'title': 'Погрузка', 'has_extension': False},
    {'title': 'Подсобка', 'has_extension': False},
    {'title': 'Сборка', 'has_extension': True},
    {'title': 'Монтаж', 'has_extension': True},
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
            # f'{self.second_name[:1]+"." if self.second_name else ""} ({self.function.post})')
            f'{self.second_name[:1]+"." if self.second_name else ""} ({self.table_num})')

    def get_short_name(self):
        return f'{self.surname} {self.name[:1]}.{self.second_name[:1]+"." if self.second_name else ""}'


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
        return f'ПР-{self.no:06}'

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

    def __str__(self):
        return f'Задача №{self.id}'
        # return f'Задача №{self.id} от {self.create_at:%d.%m.%y}'


class Period(BaseModel):
    worker = ForeignKeyField(Worker, verbose_name='Работник', backref='time_worked', on_delete='CASCADE')
    task = ForeignKeyField(Task, backref='time_worked', verbose_name='Задача', on_delete='CASCADE')
    order = ForeignKeyField(Order, backref='time_worked', null=True, verbose_name='Задача', on_delete='CASCADE')
    date = DateField(default=datetime.datetime.now().date, verbose_name='Дата')
    value = SmallIntegerField(verbose_name="Продолжительность")

    def __str__(self):
        return f'{self.date:%d.%m.%y} ({self.date:%a}) - {self.value} ч.'

    def __add__(self, other):  # обычное сложение с правым элементом
        return int(self.value + other.value) if isinstance(other, self.__class__) else (
            int(self.value + other) if isinstance(other, (int, float)) else NotImplemented)

    def __radd__(self, other):  # метод для функции sum() и сложение с левым элементом
        return int(other + self.value) if isinstance(other, (int, float)) else NotImplemented

    def get_day_week(self):
        return f'{self.date:%a}', int(f'{self.date:%w}')


class Month:
    __slots__ = ['__number', '__name', '__days', '__mean', '__start_idx']
    __ratio = {
        1: 'Январь', 2: 'Февраль', 3: 'Март',
        4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь',
        10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',
    }

    def __init__(self, number):
        error = None
        if not isinstance(number, int):
            error = f"'{self.__class__.__name__}' объект должен иметь значение в виде целого числа"
        if not 1 <= number <= 12:
            error = f"'{self.__class__.__name__}' объект не может иметь значение меньше 1 и больше 12 "
        if error:
            raise AttributeError(error)
        self.__number = number
        self.__name = self.__ratio.get(number)
        self.__start_idx, self.__days = calendar.monthrange(datetime.datetime.now().year, number)

    def __str__(self):
        return self.__name

    @property
    def number(self):
        return self.__number

    @property
    def days(self):
        return self.__days

    @property
    def start_day_idx(self):
        return self.__start_idx

    def get_means(self):
        return int(self.__days) // 2

    def lower(self):
        return self.__name.lower()

    def capitalize(self):
        return self.__name.capitalize()
