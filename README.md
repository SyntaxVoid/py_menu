# py_menu

py_menu is an easily configurable python API for creating command-line-based menu interfaces. This package is intended to be used on any python version >= 3.0.

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
This is from `add_option_example.py`
```python
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
from py_menu import Menu, Option

# We define the functions we will call to retrieve the date information
import datetime
def format_now(frmt):
  print(datetime.datetime.now().strftime(frmt))
  return

splash = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          ~!~ Date/Time example of py_menu ~!~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# We start by making all of the menus
main_menu = Menu(header = "Pick an option!", splash = splash)
time_menu = Menu(header = "Time Information")
date_menu = Menu(header = "Date Information")

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

```

# Development

Want to contribute? Great!

Feel free to fork and create a pull request! I don't bite! 
