from openpyxl import Workbook
from openpyxl.worksheet.page import PageMargins


class PersonalMonthExelTable:
    _queryset = None

    def __init__(self):
        self._book = Workbook()
        self._work_sheet = self._book.active
        self._cell = self._work_sheet.cell
        self.set_dimensions()
        self.prefill_cell()

    def set_dimensions(self):


        cm = 1 / 2.54

        #  Настройка вывода на печать
        self._work_sheet.page_setup.orientation = 'landscape'  # формат листа альбомный
        self._work_sheet.page_setup.paperSize = '9'  # лист А4

        # Отступы листа
        self._work_sheet.page_margins = PageMargins(
            left=.7 * cm,
            right=.7 * cm,
            top=int(2 * cm),
            bottom=int(.9 * cm),
            footer=0.25 * cm
        )
        self._work_sheet.print_options.horizontalCentered = True  # выравнивание таблицы на листе по центру
        self._work_sheet.print_area = self._work_sheet.calculate_dimension()  # указание массива печати

        # Задание вывода таблицы по ширине листа
        self._work_sheet.page_setup.fitToPage = True
        self._work_sheet.page_setup.fitToWidth = 1
        self._work_sheet.page_setup.fitToHeight = 1

    def prefill_cell(self):
        pass
