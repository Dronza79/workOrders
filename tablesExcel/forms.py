import datetime

from openpyxl import Workbook
from openpyxl.styles import Side, Border, Alignment, Font
from openpyxl.utils import get_column_interval
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.worksheet import Worksheet

from .template_text import TEMPLATE_ALIGNMENT_RIGHT, TEMPLATE_CLARIFICATION, TEMPLATE_TABLE


# from tablesExcel.forms import PersonalMonthExelTable


class PersonalMonthExelTable:
    _queryset = None

    def __init__(self):
        self._book: Workbook = Workbook()
        self._worksheet: Worksheet = self._book.active
        self._worksheet.title = '1'
        self.prefill_worksheet()

    def save(self):
        self._book.save('test.xlsx')

    def add_worksheet(self):
        self._worksheet = self._book.create_sheet(f'{len(self._book.sheetnames) + 1}')
        self.prefill_worksheet()

    def fill_data(self):
        self._worksheet['N9'].value = 100

    def prefill_worksheet(self):

        # задать высоту строк
        row_height = [15 for _ in range(5)]
        row_height += [18, 16.5, 16.5]
        row_height += [29.5 for _ in range(12)]
        row_height += [15 for _ in range(10)]
        for key, val in enumerate(row_height):
            # self._worksheet.row_dimensions[key + 6].height = val  # реальное значение
            self._worksheet.row_dimensions[key + 1].height = val  # реальное значение

        # задать ширину ячеек
        for idx in get_column_interval(2, 31):
            self._worksheet.column_dimensions[idx].width = 5  # значение в пикселях умноженное на 7
        self._worksheet.column_dimensions['A'].width = 6

        # объединение ячеек
        lst_range_cell = ['A6:A8', 'B6:K8', 'L6:M8', 'N6:AC6', 'AD6:AE8']
        lst_range_cell += ['A9:A10', 'B9:K10', 'L9:M10', 'AD9:AE10']
        lst_range_cell += ['A11:A12', 'B11:K12', 'L11:M12', 'AD11:AE12']
        lst_range_cell += ['A13:A14', 'B13:K14', 'L13:M14', 'AD13:AE14']
        lst_range_cell += ['A15:A16', 'B15:K16', 'L15:M16', 'AD15:AE16']
        lst_range_cell += ['A17:A18', 'B17:K18', 'L17:M18', 'AD17:AE18']
        lst_range_cell += ['A19:A20', 'B19:K20', 'L19:M20', 'AD19:AE20']
        lst_range_cell += ['W21:AC22', 'W23:AC24', 'AD21:AE22', 'AD23:AE24', 'AD25:AE26', 'AB25:AC26']
        [self._worksheet.merge_cells(range_string) for range_string in lst_range_cell]

        # границы и выравнивание в ячейках таблицы
        table = self._worksheet['A6:AE20'] + self._worksheet['AD21:AE26']
        thins = Side(border_style="thin", color="000000")
        for line in table:
            for cell in line:
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = Border(top=thins, bottom=thins, left=thins, right=thins)

        # нижнее подчеркивание
        underline = (self._worksheet['D3:G3'] + self._worksheet['L3:M3'] + self._worksheet['Q3:U3'] +
                     self._worksheet['R1:S1'] + self._worksheet['H22:M22'] + self._worksheet['H25:M25'] +
                     self._worksheet['H28:M28'])
        for line in underline:
            for cell in line:
                cell.border = Border(bottom=thins)

        # предзаполнение текста заголовка и подписей экселя
        for i, adr in enumerate(['Q1', 'K3', 'P3', 'G22', 'M22', 'G25', 'M25']):
            cell = self._worksheet[adr]
            if adr in ['M22', 'M25', 'M28']:
                cell.font = Font(size='11')
            else:
                cell.font = Font(size='14')
            cell.value = TEMPLATE_ALIGNMENT_RIGHT[i]
            cell.alignment = Alignment(horizontal='right', vertical='center')
        for adr in ['C3', 'G28']:
            cell = self._worksheet[adr]
            cell.font = Font(size='14')
            cell.value = TEMPLATE_ALIGNMENT_RIGHT[-1]
            cell.alignment = Alignment(horizontal='right', vertical='center')
        self._worksheet['T1'].alignment = Alignment(horizontal='left', vertical='center')
        self._worksheet['T1'].value = f'{datetime.datetime.now().year} года'
        self._worksheet['T1'].font = Font(size='14')

        # заполнение надстрочных пояснений
        for adr in ['D4', 'S4', 'H23', 'H26', 'H29']:
            self._worksheet[adr].font = Font(vertAlign='superscript', size='14')
            if adr != 'S4':
                self._worksheet[adr].alignment = Alignment(horizontal='left', vertical='center')
                if adr == 'D4':
                    self._worksheet[adr].value = TEMPLATE_CLARIFICATION[0]
                else:
                    self._worksheet[adr].value = TEMPLATE_CLARIFICATION[-1]
            else:
                self._worksheet[adr].alignment = Alignment(horizontal='center', vertical='center')
                self._worksheet[adr].value = TEMPLATE_CLARIFICATION[1]

        # предзаполнение таблицы
        for i, adr in enumerate(['A6', 'B6', 'L6', 'N6', 'AD6', 'W21', 'W23', 'AB25']):
            self._worksheet[adr].value = TEMPLATE_TABLE[i]
            self._worksheet[adr].font = Font(size='11')
            self._worksheet[adr].alignment += Alignment(wrapText=True)
            if adr in ['W21', 'W23', 'AB25']:
                self._worksheet[adr].alignment += Alignment(horizontal='right', vertical='center')
        for num in range(1, 32):
            if num < 16:
                cell = self._worksheet.cell(7, 13 + num)
            else:
                cell = self._worksheet.cell(8, num - 2)
            cell.value = num
            cell.font = Font(size='9')

        # перемещение строк на одну вниз
        self._worksheet.move_range('A3:U4', rows=1)

        #  Настройка вывода на печать
        self._worksheet.page_setup.orientation = 'landscape'  # формат листа альбомный
        self._worksheet.page_setup.paperSize = '9'  # лист А4

        # Отступы листа
        cm = 1 / 2.54
        self._worksheet.page_margins = PageMargins(
            left=.5 * cm,
            right=.5 * cm,
            top=1 * cm,
            bottom=1 * cm,
            footer=0.5 * cm
        )
        self._worksheet.print_options.horizontalCentered = True  # выравнивание таблицы на листе по центру
        self._worksheet.print_area = self._worksheet.calculate_dimension()  # указание массива печати

        # Задание вывода таблицы по ширине листа
        self._worksheet.page_setup.fitToPage = True
        self._worksheet.page_setup.fitToWidth = 1
        self._worksheet.page_setup.fitToHeight = 1

    def prefill_cell(self):
        pass
