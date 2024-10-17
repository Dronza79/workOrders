import PySimpleGUI as sg

table_setting = {
    'auto_size_columns': False,
    'justification': 'left',
    # 'num_rows': 10,
    'alternating_row_color': '#0E7477',
    'expand_y': True,
    'expand_x': True,
    'vertical_scroll_only': True,
    'enable_events': True,
    'row_height': 35,
    # 'font': '_ 12',
    'header_font': '_ 9',
    'header_text_color': sg.DEFAULT_BUTTON_COLOR[1],
    'header_background_color': sg.DEFAULT_BACKGROUND_COLOR,
    'header_border_width': 1,
    'enable_click_events': True,
    'pad': 0,
}

table_period_setting = {
    'auto_size_columns': False,
    'justification': 'left',
    'num_rows': 5,
    'alternating_row_color': '#0E7477',
    'expand_y': True,
    'expand_x': True,
    'vertical_scroll_only': True,
    'enable_events': True,
    'row_height': 20,
    'font': '_ 11',
    'header_font': '_ 9',
    'header_text_color': sg.DEFAULT_BUTTON_COLOR[1],
    'header_background_color': sg.DEFAULT_BACKGROUND_COLOR,
    'enable_click_events': True,
    'pad': 0,
}

table_tasks_setting = {
    'auto_size_columns': False,
    'justification': 'left',
    'alternating_row_color': '#0E7477',
    'expand_y': True,
    # 'expand_x': True,
    'vertical_scroll_only': False,
    'enable_events': True,
    'row_height': 25,
    # 'font': '_ 11',
    'header_font': '_ 9',
    'header_text_color': sg.DEFAULT_BUTTON_COLOR[1],
    'header_background_color': sg.DEFAULT_BACKGROUND_COLOR,
    'enable_click_events': True,
}

tab_group_setting = {
    # 'tab_location': None,
    'title_color': 'white',
    'tab_background_color': sg.DEFAULT_BACKGROUND_COLOR,
    'selected_title_color': 'black',
    'selected_background_color': '#F0F3F7',
    'enable_events': True,
    'expand_x': True,
    'expand_y': True,
}

tab_setting = {
    'element_justification': 'center',
}

input_setting = {
    'size': (23, 1),
    'font': ('_', 12),
    'justification': 'left',
    'pad': ((0, 0), (5, 5)),
    'disabled_readonly_background_color': sg.DEFAULT_BACKGROUND_COLOR,
    # 'text_color': 'black',
    # 'disabled_readonly_text_color': '#A3A3A3',
}

input_readonly_setting = {
    'size': (23, 1),
    'font': ('_', 12),
    'justification': 'left',
    'pad': ((0, 0), (5, 5)),
    'disabled_readonly_background_color': sg.DEFAULT_BACKGROUND_COLOR,
    # 'text_color': 'black',
    'disabled_readonly_text_color': '#A3A3A3',
}

drop_down_setting = {
    'size': (22, 1),
    'pad': ((0, 0), (5, 5)),
    'font': ('_', 12),
}

drop_down_read_only_setting = {
    'size': (22, 1),
    'pad': ((0, 0), (5, 5)),
    'readonly': True,
    'font': ('_', 12),
}

search_drop_down_setting = {
    'size': (22, 1),
    'bind_return_key': True,
    'enable_events': True,
    'pad': ((0, 0), (5, 5)),
    'font': ('_', 12),
}

drop_down_type_task_setting = {
    'size': (25, 1),
    'pad': ((0, 0), (5, 5)),
    'readonly': True,
    'font': ('_', 11),
}

text_setting = {
    'auto_size_text': None,
    'font': '_ 10',
    'pad': 0,
}

multiline_setting = {
    'size': (22, 3),
    'font': '_ 12',
    'pad': 0,
}

error_popup_setting = {
    'background_color': '#92AECE',
    'text_color': 'red',
    'line_width': 50,
    'font': '_ 12',
    'modal': True
}

info_popup_setting = {
    'button_type': 5,
    'background_color': '#92AECE',
    'auto_close': True,
    'auto_close_duration': 1,
    'non_blocking': True,
    'font': '_ 12',
    'no_titlebar': True,
}

delete_button_setting = {
    'disabled_button_color': '#4A6984 on #64778D',
    'use_ttk_buttons': True,
    'pad': ((0, 15), (15, 10)),  # (left/right, top/bottom) or ((left, right), (top, bottom))
}

frame_setting = {
    'pad': ((0, 0), (0, 15)),
    'expand_x': True,
    'expand_y': True,
    'grab': True,
    'element_justification': 'left',
    'vertical_alignment': 'center'
}

calendar_button_setting = {
    'button_text': 'Календарь',
    'format': '%d.%m.%Y',
    'begin_at_sunday_plus': 1,
}

output_setting = {
    'size': (50, 20),
    'font': '_ 12',
    'no_titlebar': True,
    'do_not_reroute_stdout': False,
    'echo_stdout': True,
    'erase_all': False,
}

title_bar_setting = {
    'text_color': None,
    'background_color': sg.DEFAULT_BACKGROUND_COLOR,
}

menu_bar_setting = {
    'bar_font': '_ 11',
    'font': '_ 11',
    'pad': ((20, 0), (0, 10)),
    'background_color': sg.DEFAULT_SCROLLBAR_COLOR,
    'text_color': sg.DEFAULT_BUTTON_COLOR[1],
    'bar_background_color': sg.DEFAULT_BACKGROUND_COLOR,
    'bar_text_color': sg.DEFAULT_BUTTON_COLOR[1],
}

logo = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAAAAlwSFlzAAAOwgAADsIBFShKgAAAABl0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xOdTWsmQAAASfSURBVFhH3Zd7iFVVFIfnYTZkYZkZaE1FY4GkqJRpETIkSNGDpJQwkoqSIAIhKILKLKN/+sOo6MVQRC8KhEpIIyJ6kGWQGVaYlQpWvl9Zvmb6vn3WOfecuffaWNIf/eBjr73W3nudu89+nNvyv1VfX98xvb29p8OdMId6e4T+vRjwBAYcGgyGtgiZuJX4hfAsbKDeR/kxRUc0OTLR0V8yGm6El+Ar2AY7YQ98BxfRrp2yC3pgL6hN8AnMIH4c5SjbxdB/LzqMg8XwC/TSuSJcb8N5cCzcCxvD7wM8DGOodsBt2B/BWuzxMXxz0WgojR+g3AF1IuYvvw/T6Z4AS0FthefhDDgZboY1Wa8kx+uMNI1Fg+Pp9BYcSl36Cf9vFNPAKZ0Lm+EgfAkTw38FfKM/+igfeiHVdol0VdHAp15ip0Yitg6mYJ5E+Vz4DsAjmM6aa+Bl+NOYwt4PL0I3OP5N8BRMjrSZaOsiehLq3rXC/QO4GM+BL0A5G9eBv/pqSKteYZt4OVwMI+AO+BnyWbk7UmfCcSUcSL37Cf8uivGUU8CFpG89nA8uwCdgr36F7azMw3SmpoI7pzI29bGROiUfAu9FrCL8u+AymA7bw7cKnImzYGlqGKL+GeSv6UHYnUVqij61dYDDlbw/C9eE7xDcBc7OzvC5qjspL4ANkF4ZhVP+DKaJR8IH0Gjr7obpkToTjkURrwj/a+Di2RT17eBr8IF+TY0QtttvLmYH5eXwUxapF7GnKQZF6uKk+z5FS8Lnr5uKmc4CbA8Xt9e1sEefwnYtXIo5mPJ2KO+AP8CTsJgJzBsidSYco2BLxJOiwz0UH2ae5HscTL45XPrWwIQYx/ddPJii/iPFmWU/dk9KnAuHx2XlxLMjvBtVtYK673xb1G2zEkZjerDMxy5WObZaC5dEjhmQ1gtyAbam5ArHWEgLLBf1LZDv160U0yjLe/xrik7w7HgM9qUAwnYLvoppPCWibMN3NizGXgG1NYCz7gHKIvYOlF/F53Cafan6morkufB5Uy6BrsgxBpaBO8Crubi+DfpkxdSWhf93MGG6Fyh9512Y/vJbodHWdUesCtvXNAxWpyDCfjNSZ8LnGV5sqbLwe8nkyX0F6SrF9tzw1VSEzwvJ2zCNR+nie4GyuNiwF6TEZeFsegEp4h4yM21L1dtyZRYptAPfK7AIKrco9fIWVN0paVk4rzcS7SoK/3xIC4rqLZAvUGfIY3kmvA9166Es4p4Zw1LSsogNJ5Aumf7Cb4IR0a4N3HLuEo9aPzh9oOIdH06066Go7YBcON0mD0FlFqyjWdEsCbfHrff6ueDn2mF/dS7auaAnxjD1Iuig30b7JOpO2ZBokoTbi8h3ne6HgYr298cQzUWjSVA+7Uzid4Df916xj+qDhuulmWjuqXpipGkuGvkqroLyheI3nzNRd68PRPT7FE6NFAMT/Tx6K6/jSEV/t+7rMDKGHbjo7+f2KeDHoyu+4RdyI9F2H/jxOpvqP/s3lIsBWsE14J8O7/WmK57YRngDZkPatkdNjO+DDGJgt941MA8WgA/mf4Nu4v5PPHp/QP8btbT8Bcysd8LaK8+vAAAAAElFTkSuQmCC'
