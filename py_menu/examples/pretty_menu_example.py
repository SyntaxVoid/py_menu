
"""
This example uses the same menu created in add_option_example.py to highlight
the Menu.pretty_menu feature. For help on how the menu was created, please
refer to add_option_example.py
"""

import datetime
def format_now(frmt):
  """ Formats the current time according to the frmt string """
  print(datetime.datetime.now().strftime(frmt))
  return

from py_menu import Menu

splash = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~!~ Date/Time example of py_menu ~!~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# The menu creation is documented and explained in add_option_example.py
main_menu = Menu(header="Pick an option!", splash=splash)
time_menu = Menu(header="Time Information")
date_menu = Menu(header="Date Information")
main_menu.add_option("Time Information", time_menu)
main_menu.add_option("Date Information", date_menu)
time_menu.add_option("Display Current Hour", lambda: format_now("%H"))
time_menu.add_option("Display Current Minute", lambda: format_now("%M"))
time_menu.add_option("Display Current Second", lambda: format_now("%S"))
time_menu.add_option("Display Current Time", lambda: format_now("%H:%M:%S"))
date_menu.add_option("Display Current Month", lambda: format_now("%B"))
date_menu.add_option("Display Current Day", lambda: format_now("%d"))
date_menu.add_option("Display Current Year", lambda: format_now("%y"))
date_menu.add_option("Display Current Date", lambda: format_now("%B %d, %y"))

print(main_menu.pretty_menu())

# Output below
"""
 | 1. Time Information
 |     >---| 1. Display Current Hour
 |         | 2. Display Current Minute
 |         | 3. Display Current Second
 |         | 4. Display Current Time
 |
 | 2. Date Information
 |     >---| 1. Display Current Month
 |         | 2. Display Current Day
 |         | 3. Display Current Year
 |         | 4. Display Current Date
 |
"""
