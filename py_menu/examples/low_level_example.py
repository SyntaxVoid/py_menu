"""
For this example, we'll be creating a very basic menu capable of displaying
the date and time information. This is a LOW_LEVEL implementation. This example
might be useful to you if you are dynamically producing your Options and menus. 
Because things have to be declared in opposite order, this way can be hard to
read. 
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

# First, we import the Option and Menu class
from py_menu import Option, Menu

# We define the functions we will call to retrieve the date information
import datetime
def format_now(frmt):
  print(datetime.datetime.now().strftime(frmt))
  return

# Because higher level menus need to reference the lower level menus, we need
# to define the lower level Options/Menus first. 
# TIP: If you need to pass arguments to your action, use a lambda!

# TIME OPTIONS + TIME MENU
hour_opt   = Option("Display Current Hour", lambda: format_now("%H"))
minute_opt = Option("Display Current Minute", lambda: format_now("%M"))
second_opt = Option("Display Current Second", lambda: format_now("%S"))
cur_time_opt = Option("Display Current Time", lambda: format_now("%H:%M:%S"))
time_options = [hour_opt, minute_opt, second_opt, cur_time_opt]
time_menu = Menu("Time Menu", options = time_options)

# DATE OPTIONS + DATE MENU
month_opt = Option("Display Current Month", lambda: format_now("%B"))
day_opt = Option("Display Current Day", lambda: format_now("%d"))
year_opt = Option("Display Current Year", lambda: format_now("%y"))
cur_date_opt = Option("Display Current Date", lambda: format_now("%B %d, %y"))
date_options = [month_opt, day_opt, year_opt, cur_date_opt]
date_menu = Menu("Date Menu", options = date_options)

# Now, we have to put the time and date menu into the MAIN menu!!
# We have to make an Option for the Time menu and the Date menu. Instead of
# adding a function, we add the appropriate Menu object! 
main_time_option = Option("Time Information", time_menu)
main_date_option = Option("Date Information", date_menu)
main_options = [main_time_option, main_date_option]
splash = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~!~ Date/Time example of py_menu ~!~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
main_menu = Menu("Date/Time Menu", main_options, splash)

# And then to run our Menu, we call the mainloop method!
main_menu.mainloop()
