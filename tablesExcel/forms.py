import datetime

from openpyxl import Workbook
from openpyxl.styles import Side, Border, Alignment, Font, PatternFill
from openpyxl.utils import get_column_interval
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.worksheet import Worksheet

from .template_text import TEMPLATE_ALIGNMENT_RIGHT, TEMPLATE_CLARIFICATION, TEMPLATE_TABLE


# from tablesExcel.forms import PersonalMonthExelTable


class PersonalMonthExelTable:
    def __init__(self):
        self._book: Workbook = Workbook()
        self._worksheet: Worksheet = self._book.active
        self._worksheet.title = '1'
        self.prefill_worksheet()

    def save(self, file_name='test'):
        try:
            name = f'{file_name}.xlsx'
            self._book.save(name)
        except PermissionError:
            name = f'{file_name}-copy.xlsx'
            self._book.save(name)
        return name

    def add_worksheet(self):
        self._worksheet = self._book.create_sheet(f'{len(self._book.sheetnames) + 1}')
        self.prefill_worksheet()

    def fill_data(self, worker, month, calc, target, data_task, data_old_task):
        offset = 0
        for num in range(1, month.days + 1):
            if num < 16:
                cell = self._worksheet.cell(7, 13 + num)
            else:
                cell = self._worksheet.cell(8, num - 2)
            cell.value = num
            cell.font = Font(size='9')
        self._worksheet.cell(4, 28).value = target
        self._worksheet.cell(4, 28).alignment = Alignment(horizontal='center', vertical='center')
        self._worksheet.cell(1, 18).value = str(month).lower()
        self._worksheet.cell(4, 4).value = worker.get_short_name()
        self._worksheet.cell(4, 4).alignment = Alignment(horizontal='center', vertical='center')
        self._worksheet.cell(4, 12).value = worker.table_num
        self._worksheet.cell(4, 12).alignment = Alignment(horizontal='center', vertical='center')
        self._worksheet.cell(4, 17).value = worker.function.post
        self._worksheet.cell(4, 17).alignment = Alignment(horizontal='center', vertical='center')
        self._worksheet.cell(28, 13).value = worker.get_short_name()
        self._worksheet.cell(21, 30).value = sum(calc.get('first_half', 0))
        self._worksheet.cell(23, 30).value = sum(calc.get('second_half', 0))
        for i, task in enumerate(data_task):
            self._worksheet.cell(9 + offset + i, 1).value = i + 1
            data_string = f'{task.is_type} '
            data_string += f'{task.order}\n' if task.order else '\n'
            data_string += f'{task.order.type_obj} {task.order.title} {task.order.name}\n' if task.order else ''
            data_string += f'{task.order.article}' if task.order else f'{task.comment}'
            self._worksheet.cell(9 + offset + i, 2).value = data_string
            self._worksheet.cell(9 + offset + i, 2).alignment += Alignment(wrapText=True)
            self._worksheet.cell(9 + offset + i, 12).value = task.deadline - sum(data_old_task[i].time_worked)
            self._worksheet.cell(9 + offset + i, 32).value = sum(data_old_task[i].time_worked)
            self._worksheet.cell(9 + offset + i, 30).value = sum(task.time_worked)
            for period in task.time_worked:
                if period.date.day <= 15:
                    self._worksheet.cell(9 + offset + i, 13 + period.date.day).value = period.value
                else:
                    self._worksheet.cell(9 + offset + i + 1, period.date.day - 2).value = period.value
            offset += 1

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
        lst_range_cell += ['D4:G4', 'l4:M4', 'Q4:U4', 'AB4:AC4', 'R1:S1']
        [self._worksheet.merge_cells(range_string) for range_string in lst_range_cell]

        # границы и выравнивание в ячейках таблицы
        table = self._worksheet['A6:AE20'] + self._worksheet['AD21:AE26']
        thins = Side(border_style="thin", color="000000")
        for line in table:
            for cell in line:
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = Border(top=thins, bottom=thins, left=thins, right=thins)

        # нижнее подчеркивание
        underline = (self._worksheet['D4:G4'] + self._worksheet['L4:M4'] + self._worksheet['Q4:U4'] +
                     self._worksheet['R1:S1'] + self._worksheet['H22:M22'] + self._worksheet['H25:M25'] +
                     self._worksheet['H28:M28'] + self._worksheet['AB4:AC4'])
        for line in underline:
            for cell in line:
                cell.border = Border(bottom=thins)

        # предзаполнение текста заголовка и подписей экселя
        for i, adr in enumerate(['Q1', 'K4', 'P4', 'AA4', 'G22', 'M22', 'G25', 'M25', 'M28']):
            cell = self._worksheet[adr]
            if adr in ['M22', 'M25', 'M28']:
                cell.font = Font(size='11')
            else:
                cell.font = Font(size='14')
            if adr != 'M28':
                cell.value = TEMPLATE_ALIGNMENT_RIGHT[i]
            cell.alignment = Alignment(horizontal='right', vertical='center')
        for adr in ['C4', 'G28']:
            cell = self._worksheet[adr]
            cell.font = Font(size='14')
            cell.value = TEMPLATE_ALIGNMENT_RIGHT[-1]
            cell.alignment = Alignment(horizontal='right', vertical='center')
        self._worksheet['T1'].alignment = Alignment(horizontal='left', vertical='center')
        self._worksheet['T1'].value = f'{datetime.datetime.now().year} года'
        self._worksheet['T1'].font = Font(size='14')

        # заполнение надстрочных пояснений
        for adr in ['D5', 'S5', 'H23', 'H26', 'H29']:
            self._worksheet[adr].font = Font(vertAlign='superscript', size='14')
            if adr != 'S5':
                self._worksheet[adr].alignment = Alignment(horizontal='left', vertical='center')
                if adr == 'D5':
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
        self._worksheet['AD25'] = '=SUM(AD21:AE24)'

        # заливка ячеек таблицы
        range_cell = []
        for adr in range(8, 21, 2):
            range_cell += self._worksheet[f'N{adr}:AC{adr}']
        for line in range_cell:
            for cell in line:
                cell.fill = PatternFill(fill_type='solid', fgColor="DDDDDD")

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
