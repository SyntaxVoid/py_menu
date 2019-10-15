"""
For this example, we'll be creating a very basic menu capable of displaying
the date and time information. We will be creating the same Menu from
low_level_example.py but we will be using the Menu.add_option method which
improves the readability!

For this example, the layout of the menu is as follows:

  | 1. Time information---|
  |                       | 1. Display Current Hour    |
  |                       | 2. Display Current Minute  | This is the
  |                       | 3. Display Current Second  | Time menu
  |                       | 4. Display Current Time    |
  |
  | 2. Date Information---|
  |                       | 1. Display Current Month   |
  |                       | 2. Display Current Day     | This is the
  |                       | 3. Display Current Year    | date menu
  |                       | 4. Display Current Date    |
  |                       |

"""


# We define the functions we will call to retrieve the date information
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

# We start by making all of the menus
main_menu = Menu(header="Pick an option!", splash=splash)
time_menu = Menu(header="Time Information")
date_menu = Menu(header="Date Information")

# We can add the secondary menus to the main menu now. The arguments passed to
# menu.add_option are the same as you would use when creating an Option object.
main_menu.add_option("Time Information", time_menu)
main_menu.add_option("Date Information", date_menu)

# Now we add the options to the time and date menus. This can be done before or
# after the previous step. Once the initial menu object are created, options
# can be added at any time.
time_menu.add_option("Display Current Hour", lambda: format_now("%H"))
time_menu.add_option("Display Current Minute", lambda: format_now("%M"))
time_menu.add_option("Display Current Second", lambda: format_now("%S"))
time_menu.add_option("Display Current Time", lambda: format_now("%H:%M:%S"))

date_menu.add_option("Display Current Month", lambda: format_now("%B"))
date_menu.add_option("Display Current Day", lambda: format_now("%d"))
date_menu.add_option("Display Current Year", lambda: format_now("%y"))
date_menu.add_option("Display Current Date", lambda: format_now("%B %d, %y"))

# And then we start the mainloop!
main_menu.mainloop()

# MUCH easier to understand compared to the low level example!
