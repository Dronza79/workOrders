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
    # 'size': (6, 1),
    'font': ('_', 12),
    'justification': 'left',
    'pad': ((0, 0), (5, 5)),
    'disabled_readonly_background_color': sg.DEFAULT_BACKGROUND_COLOR,
}

ord_setting = {
    'size': (6, 1),
    'font': ('_', 12),
    'justification': 'left',
    'pad': ((0, 0), (5, 5)),
    'disabled_readonly_background_color': sg.DEFAULT_BACKGROUND_COLOR,
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
    'keep_on_top': True,
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
    'keep_on_top': True,
}

delete_button_setting = {
    'disabled_button_color': '#4A6984 on #64778D',
    'use_ttk_buttons': True,
    'pad': ((0, 15), (15, 10)),  # (left/right, top/bottom) or ((left, right), (top, bottom))
}

frame_setting = {
    'pad': 0,
    'expand_x': True,
    'expand_y': True,
    'grab': True,
    'element_justification': 'center',
    'vertical_alignment': 'center',
}


horizontal_col_setting = {
    'expand_x': True,
    'pad': 0,
    'justification': 'c',
    'element_justification': 'c',
    'vertical_alignment': 'c'
}


card_setting = {
    'expand_y': True,
    'expand_x': True,
    'pad': 0,
    'justification': 'c',
    'element_justification': 'c',
    'vertical_alignment': 'c'
}


table_frame_setting = {
    'pad': ((0, 0), (0, 15)),
    'expand_x': True,
    'expand_y': True,
    'grab': True,
    'element_justification': 'center',
    'vertical_alignment': 'center',
}

frame_padding_0_setting = {
    'pad': 0,
    'expand_x': True,
    'expand_y': True,
    'grab': True,
    'element_justification': 'center',
    'vertical_alignment': 'center',
}

calendar_button_setting = {
    'button_text': 'Календарь',
    'format': '%d.%m.%Y',
    'begin_at_sunday_plus': 1,
    'size': (10, 1)
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

menu_setting = {
    'background_color': sg.DEFAULT_SCROLLBAR_COLOR,
    'text_color': sg.DEFAULT_BUTTON_COLOR[1],
    # 'disabled_text_color': None,
    # 'size': (None, None),
    # 'tearoff': False,
    'font': '_ 11',
    'pad': ((0, 0), (0, 5)),
    # 'visible': True,
}

menu_bar_setting = {
    'bar_font': '_ 11',
    'font': '_ 11',
    'pad': ((0, 0), (0, 5)),
    'background_color': sg.DEFAULT_SCROLLBAR_COLOR,
    'text_color': sg.DEFAULT_BUTTON_COLOR[1],
    'bar_background_color': sg.DEFAULT_BACKGROUND_COLOR,
    'bar_text_color': sg.DEFAULT_BUTTON_COLOR[1],
}

get_data_popup_setting = {
    'return_keyboard_events': True,
    'grab_anywhere': True,
    'finalize': True,
    'modal': True,
    'keep_on_top': True,
    'margins': (0, 0)
}

logo_w = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAAAAlwSFlzAAAOwgAADsIBFShKgAAAABl0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xOdTWsmQAAASfSURBVFhH3Zd7iFVVFIfnYTZkYZkZaE1FY4GkqJRpETIkSNGDpJQwkoqSIAIhKILKLKN/+sOo6MVQRC8KhEpIIyJ6kGWQGVaYlQpWvl9Zvmb6vn3WOfecuffaWNIf/eBjr73W3nudu89+nNvyv1VfX98xvb29p8OdMId6e4T+vRjwBAYcGgyGtgiZuJX4hfAsbKDeR/kxRUc0OTLR0V8yGm6El+Ar2AY7YQ98BxfRrp2yC3pgL6hN8AnMIH4c5SjbxdB/LzqMg8XwC/TSuSJcb8N5cCzcCxvD7wM8DGOodsBt2B/BWuzxMXxz0WgojR+g3AF1IuYvvw/T6Z4AS0FthefhDDgZboY1Wa8kx+uMNI1Fg+Pp9BYcSl36Cf9vFNPAKZ0Lm+EgfAkTw38FfKM/+igfeiHVdol0VdHAp15ip0Yitg6mYJ5E+Vz4DsAjmM6aa+Bl+NOYwt4PL0I3OP5N8BRMjrSZaOsiehLq3rXC/QO4GM+BL0A5G9eBv/pqSKteYZt4OVwMI+AO+BnyWbk7UmfCcSUcSL37Cf8uivGUU8CFpG89nA8uwCdgr36F7azMw3SmpoI7pzI29bGROiUfAu9FrCL8u+AymA7bw7cKnImzYGlqGKL+GeSv6UHYnUVqij61dYDDlbw/C9eE7xDcBc7OzvC5qjspL4ANkF4ZhVP+DKaJR8IH0Gjr7obpkToTjkURrwj/a+Di2RT17eBr8IF+TY0QtttvLmYH5eXwUxapF7GnKQZF6uKk+z5FS8Lnr5uKmc4CbA8Xt9e1sEefwnYtXIo5mPJ2KO+AP8CTsJgJzBsidSYco2BLxJOiwz0UH2ae5HscTL45XPrWwIQYx/ddPJii/iPFmWU/dk9KnAuHx2XlxLMjvBtVtYK673xb1G2zEkZjerDMxy5WObZaC5dEjhmQ1gtyAbam5ArHWEgLLBf1LZDv160U0yjLe/xrik7w7HgM9qUAwnYLvoppPCWibMN3NizGXgG1NYCz7gHKIvYOlF/F53Cafan6morkufB5Uy6BrsgxBpaBO8Crubi+DfpkxdSWhf93MGG6Fyh9512Y/vJbodHWdUesCtvXNAxWpyDCfjNSZ8LnGV5sqbLwe8nkyX0F6SrF9tzw1VSEzwvJ2zCNR+nie4GyuNiwF6TEZeFsegEp4h4yM21L1dtyZRYptAPfK7AIKrco9fIWVN0paVk4rzcS7SoK/3xIC4rqLZAvUGfIY3kmvA9166Es4p4Zw1LSsogNJ5Aumf7Cb4IR0a4N3HLuEo9aPzh9oOIdH06066Go7YBcON0mD0FlFqyjWdEsCbfHrff6ueDn2mF/dS7auaAnxjD1Iuig30b7JOpO2ZBokoTbi8h3ne6HgYr298cQzUWjSVA+7Uzid4Df916xj+qDhuulmWjuqXpipGkuGvkqroLyheI3nzNRd68PRPT7FE6NFAMT/Tx6K6/jSEV/t+7rMDKGHbjo7+f2KeDHoyu+4RdyI9F2H/jxOpvqP/s3lIsBWsE14J8O7/WmK57YRngDZkPatkdNjO+DDGJgt941MA8WgA/mf4Nu4v5PPHp/QP8btbT8Bcysd8LaK8+vAAAAAElFTkSuQmCC'
logo_b = b'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'
