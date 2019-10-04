# py_menu

py_menu is an easily configurable python API for creating command-line-based menu interfaces. This package is intended to be used on any python version >= 2.7.

### Installation
Installation is simple! Activate your prefered python environment, if you want, and then run:
```sh
python -m pip install py_menu
```

Once installed, you can `import py_menu` anywhere!

### Getting Started
There should be several examples in the `py_menu/py_menu/examples` directory that you can run. If you wanted to run `low_level_example.py`, then simply open a python interpretter and enter:
```python
import py_menu.examples.low_level_example
```
You will immediately see an example Date/Time menu:
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~!~ Date/Time example of py_menu ~!~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Date/Time Menu
     1. Time Information
     2. Date Information
     q. Quit program
>>
```

Play around, but the interface here is pretty self explanatory. 

### Included Classes
The py_menu API exposes two classes available for use by the developer: Option and Menu. Options are used as entries to a larger Menu whereas the Menu is displayed to the user.

#### Option
Usage: `Option(name, action[, flags])`:
* `name`: type `str` - The name of the option. This will be displayed.
* `action`: callable or type `Menu` - The action to take when this option is selected. If it is a callable, it will be `__call__`-ed. If it is a `Menu` object, control will be transfered to this `Menu` and whatever the current `Menu` was will be set as the previous `Menu`. [This is an implementation detail in `Menu`!!!]
* `flags`: Not implemented for the base `Option` and `Menu` classes. The definition of flags can be set by whoever inherits from Option or Menu.

```python
opt1 = Option("This is Option1", action = lambda: print("Hello!"))
```

#### Menu
Usage: `Menu(header, [options=None, splash=""]):`
* `heade`r: type `str` - The message to be displayed at the top of the menu.
* `options`: `[Option]` - A list of Option objects to be displayed.
* `splash`: type `str` - A single message to display when mainloop begins. For nested Menu objects, the splash message will ONLY be printed for the initial object that calls mainloop. 

```python
menu1 = Menu("Pick an option!", [opt1], splash = "Welcome to the Menu!")
```


#### Full Example
This is from `low_level_example.py`
```python
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

```

# Development

Want to contribute? Great!

Feel free to fork and create a pull request! I don't bite! 
