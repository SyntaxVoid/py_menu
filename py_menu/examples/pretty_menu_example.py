
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
 | 1. Time Information [flags=0]
 |     >---| 1. Display Current Hour [flags=0]
 |         | 2. Display Current Minute [flags=0]
 |         | 3. Display Current Second [flags=0]
 |         | 4. Display Current Time [flags=0]
 |
 | 2. Date Information [flags=0]
 |     >---| 1. Display Current Month [flags=0]
 |         | 2. Display Current Day [flags=0]
 |         | 3. Display Current Year [flags=0]
 |         | 4. Display Current Date [flags=0]
 |
"""
