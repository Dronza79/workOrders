from openpyxl import Workbook
from openpyxl.styles import Side, Border, Alignment
from openpyxl.utils import get_column_interval
from openpyxl.worksheet.page import PageMargins

# from tablesExcel.models import PersonalMonthExelTable


class PersonalMonthExelTable:
    _queryset = None

    def __init__(self):
        self._book = Workbook()
        self._work_sheet = self._book.active
        self._cell = self._work_sheet.cell
        self.prefill_cell()
        self.set_dimensions()

    def save(self):
        self._book.save('test.xlsx')

    def set_dimensions(self):

        # задать высоту строк
        row_height = [18, 16.5, 16.5]
        row_height += [29.5 for _ in range(12)]
        row_height += [30, 30, 30]
        for key, val in enumerate(row_height):
            # print(f'{key=} {val=}')
            self._work_sheet.row_dimensions[key + 6].height = val  # реальное значение

        # задать ширину ячеек
        for idx in get_column_interval(2, 31):
            # print(f'{idx=}')
            self._work_sheet.column_dimensions[idx].width = 5  # значение в пикселях умноженное на 7
        self._work_sheet.column_dimensions['A'].width = 6

        # объединение ячеек
        lst_range_cell = ['A6:A8', 'B6:K8', 'L6:M8', 'N6:AC6', 'AD6:AE8']
        lst_range_cell += ['A9:A10', 'B9:K10', 'L9:M10', 'AD9:AE10']
        lst_range_cell += ['A11:A12', 'B11:K12', 'L11:M12', 'AD11:AE12']
        lst_range_cell += ['A13:A14', 'B13:K14', 'L13:M14', 'AD13:AE14']
        lst_range_cell += ['A15:A16', 'B15:K16', 'L15:M16', 'AD15:AE16']
        lst_range_cell += ['A17:A18', 'B17:K18', 'L17:M18', 'AD17:AE18']
        lst_range_cell += ['A19:A20', 'B19:K20', 'L19:M20', 'AD19:AE20']
        lst_range_cell += ['AD21:AE21', 'AD22:AE22', 'AD23:AE23']
        [self._work_sheet.merge_cells(range_string) for range_string in lst_range_cell]

        # границы и выравнивание в ячейках
        table = self._work_sheet['A6:AE20'] + self._work_sheet['AD21:AE23']
        thins = Side(border_style="thin", color="000000")
        for line in table:
            for cell in line:
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = Border(top=thins, bottom=thins, left=thins, right=thins)

        cm = 1 / 2.54

        #  Настройка вывода на печать
        self._work_sheet.page_setup.orientation = 'landscape'  # формат листа альбомный
        self._work_sheet.page_setup.paperSize = '9'  # лист А4

        # Отступы листа
        self._work_sheet.page_margins = PageMargins(
            left=.7 * cm,
            right=.7 * cm,
            top=2 * cm,
            bottom=.9 * cm,
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
