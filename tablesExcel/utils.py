import re
from pathlib import Path

from openpyxl.worksheet.page import PageMargins


def global_print_setting(worksheet, left=.5, right=.5, top=1, bottom=1, footer=0.5, header=.5):
    cm = 1 / 2.54

    worksheet.page_setup.orientation = 'landscape'  # формат листа альбомный
    worksheet.page_setup.paperSize = '9'  # лист А4

    worksheet.page_margins = PageMargins(
        left=left * cm, right=right * cm, top=top * cm, bottom=bottom * cm, footer=footer * cm, header=header * cm)
    worksheet.print_options.horizontalCentered = True  # выравнивание таблицы на листе по центру
    worksheet.print_area = worksheet.calculate_dimension()  # указание массива печати

    worksheet.page_setup.fitToPage = True
    worksheet.page_setup.fitToWidth = 1

    return worksheet


def check_path_new_file(path):
    if not Path(path).exists():
        return path
    if num := re.search(r'\d+(?=\.xlsx$)', str(path)):
        num = int(num.group())
        new_path = re.sub(r'\d+(?=\.xlsx$)', f'{num + 1}', str(path))
    else:
        new_path = Path(path).with_name(f'{Path(path).stem}-1{Path(path).suffix}')
    return check_path_new_file(new_path)
