import locale
from pathlib import Path

from database.app_logger import add_logger_peewee
from database.migrations import apply_migrations
from database.settings import path
from gui.views import StartMainWindow


# @add_logger_peewee
def main():
    # print(f'{path.get_path=}')
    # print(locale.getlocale())
    locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))
    # locale.setlocale(locale.LC_TIME, 'ru_RU')
    # print(locale.getlocale())
    if not Path(path.get_path).exists():
        apply_migrations()
    StartMainWindow()


# TODO 
# 1.	Добавить модель "Тип задачи" +
# 2.	Номер Ордера сделать строкой
# 3.	Сделать возможность добавления задачи непосредственно из карточки работника и карточки ПРки.
# 4.	Реализовать настройки программы (задание должностей и статусов задач и возможность выбора функции статуса) +
# 5.	Оперативная информация за текущий месяц
# 6.	Добавить фильтр ПРок в карточку задач
# 7.	Добавить тип задачи "Погрузо-разгрузочные работы", "Подсобные работы" +
# 8.	Получить информацию о проработанных работником часах за конкретный день
# 9.	Вывод количества отработанных часов за указанный период по всем работникам
# 10.	Добавить конфиги к моделям "Статус", "Должность", «Тип задачи» +


# data = list(Order.select())
# layout = [[sg.Combo(data,
#                     enable_events=True,
#                     # default_value="отсутствует",
#                     bind_return_key=True,
#                     key='-ODR1-')],
#           [sg.Combo(data,
#                     enable_events=True,
#                     # default_value="отсутствует",
#                     bind_return_key=True,
#                     key='-ODR2-')],
#           ]

# win = sg.Window('Проба', layout, finalize=True)
#
# while True:
#     ev, val = win.read()
#     print(f'{ev=} {val=}')
#     if ev == sg.WIN_CLOSED:
#         break
#     elif ev == '-ODR1-' and not isinstance(val[ev], Order):
#         search = val[ev]
#         print(f'{search=}')
#         new_data = list(Order.select().where(Order.article.contains(search)))
#         print(f'{new_data=}')
#         win['-ODR1-'].update(values=new_data)
#         win.refresh()
#     elif ev == '-ODR2-' and not isinstance(val[ev], Order):
#         search = int(re.sub(r'\D', '', val[ev]))
#         print(f'{search=}')
#         new_data = list(Order.select().where(Order.no == search))
#         print(f'{new_data=}')
#         win['-ODR2-'].update(new_data)
#         win.refresh()
#
# win.close()

if __name__ == '__main__':
    main()
    
