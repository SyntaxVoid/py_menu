""" Implements Menu and Option class """

import os
import platform
import sys
import subprocess
import textwrap


getch = input # default, overwrite it below if possible.
try:                             # msvrct.getch is exclusive to windows, but
  from msvcrt import getch     # its effects can be emulated in *nix. If
except ImportError:              # there are any problems setting getch, it
  try:                         # will default to 'input'.
    import tty
    import termios
    def getch():
      """ Will get one character from user without displaying it """
      file_desc = sys.stdin.fileno()
      old_attr = termios.tcgetattr(fd)
      try:
        tty.setraw(file_desc)
        _ = sys.stdin.read(1)
      finally:
        termios.tcsetattr(file_desc, termios.TCSADRAIN, old_attr)
      return ch
    except:
      pass
except:
  pass


def clear_screen():
  """ Try to clear the screen. If it fails, do nothing... No big deal """
  command = "cls" if platform.system().lower() == "windows" else "clear"
  return subprocess.call(command, shell=True)


def print2(*s, sep=" ", end="\n", file=sys.stdout, flush=True, n=60, spaces=0):
  """
  Used as the default 'print' command anytime things are displayed in Menu. The
  main benefit of this function is that all output will be formatted so that
  no line is longer than n-characters long. With that said, the developer does
  not have to worry about formatting their output messages to look 'pretty'.
  This function does that for you. Use this just as you would the normal print
  function.

  Inputs:
    *s: anything - Items to print.
    sep: str - Separator to place between each item in *s
      default = " " (A space)
    end: str - Character to print after printing everything in *s
      default = "\n" (A new line)
    file: file object or file descriptor - Location to print to.
      default = sys.stdout (Standard output stream)
    n: int - The maximum length to format each line of text to.
      default = 60
    spaces: int: The number of spaces to place *before* each element in *s.
      default = 0

  Outputs: Returns None but writes whatever is inside *s to the specified file.
  """
  for m, obj in enumerate(s, 1):
    obj = str(obj) # In case it isn't already a string
    original_lines = obj.splitlines()
    output_lines = []
    for line in original_lines:
      if line == "":
        output_lines += [""]
      else:
        output_lines += textwrap.wrap(line, width=n - spaces)
    to_print = " "*spaces + ("\n" + " "*spaces).join(output_lines)
    print(to_print, end=sep if m != len(s) else end, file=file, flush=flush)
  return


def cin(prompt=">> ", default="q", raw=False):
  """
  A general prompt for operator input. Kind of simulates a terminal. Will
  display whatever prompt is (with no newlines, unless they are explicitly in
  prompt) and accept input from the operator. If the user enteres nothing or
  whitespaces only, then the prompt will be re-printed (just like a terminal).
  In the case that the operator enters Ctrl+D (EOF) or Ctrl+C (KBI), the
  default is returned.

    Inputs:
      prompt: str - The message to display when asking for input
      default: str - The string to be returned in the event of EOF or KBI
      raw: bool - If this is True, will return any leading or trailing
                  whitespace. Otherwise will return the stripped input.
  """
  try:
    while True:
      choice = input(prompt)
      if choice.strip() == "":
        continue
      if raw:
        return choice
      return choice.strip()
  except (EOFError, KeyboardInterrupt):
    return default


def any_key_to_continue(msg=" --- Press any key to continue --- "):
  """ Displays msg and waits for a single keypress before continuing """
  print2(msg)
  getch()
  print2()
  return


class Option(object):
  """ Small class to help represent an 'Option' for a 'Menu' """
  def __init__(self, name, action, flags=0):
    """
    Initializes an Option object. This will be displayed by Menu.

    Inputs:
      name: str - The name of the option. This will be displayed
      action: callable or Menu object - The action to take when this option is
              selected. If it is a callable, it will be __call__-ed. If it is a
              Menu object, control will be transfered to this Menu and whatever
              the current Menu was will be set as the previous menu.
              [This is an implementation detail in Menu!!!]
      flags: Not implemented for the base Option and Menu classes. The
             definition of flags can be set by whoever inherits from Option
             or Menu.
    """
    self.name = name
    self.action = action
    self.flags = flags
    return


class Menu(object):
  """
  This class provides the functionality to run a command-line-interfact of a
  menu driven program. That is, a program which presents the operator with
  options and runs specified commands or displays additional lower-level menus
  when the operator makes a selection. See the examples folder for help.

  This class may be inheritted from if you require more control over your menu.
  One common feature may be to override the __str__ method to implement
  handling project-specific flags from the Option class.
  """
  def __init__(self, header, options=None, splash="", ):
    """
    Initializer for Menu objects. Provides an easily adaptable framework for
    creating command-line-interface menus.

    Inputs:
      header: str - The message to be displayed at the top of the menu.
      options: [Option] - A list of Option objects to be displayed.
      splash: str - A single message to display when mainloop begins. For
              nested Menu objects, the splash message will ONLY be printed
              for the initial object that calls mainloop.
    """
    self.header = header
    self.active_menu = self
    self.prev_menu = None
    self.options = []
    options = [] if options is None else options
    for option in options:
      self.add_option(option) # This is where self.options is built
    self.splash = splash
    self._splash_shown = False
    self.valid_options = []
    return

  def __str__(self):
    out = ""
    out += self.active_menu.header + "\n"
    opt_str = "    {option_num:2d}. {option_name}\n"
    q_str = "     q. {msg}\n"
    for option_num, option in enumerate(self.active_menu.options, start=1):
      out += opt_str.format(option_num=option_num, option_name=option.name)
      self.valid_options.append(str(option_num))
    if self.active_menu.prev_menu is None:
      out += q_str.format(msg="Quit program")
    else:
      out += q_str.format(msg="Previous menu")
    self.valid_options.append("q")
    return out

  def get_choice(self):
    """ Gets a single choice from the user """
    while True:
      choice = cin(default="q").lower()
      if choice in self.valid_options:
        return choice
      print2("$$ Invalid option! Try again.", spaces=2)
    return

  def mainloop(self):
    """ Activates the menu and handles user input """
    if not self._splash_shown:
      # In case something subclasses this Menu, there are sometimes cases where
      # the mainloop needs to be temporarily exitted from (from a custom
      # exception) and then restarted. In those cases, the mainloop may be
      # called several times. The splash message should not be displayed in
      # those cases.
      clear_screen()
      print2(self.splash)
      self._splash_shown = True
    while True:
      print2(self)
      choice = self.get_choice()
      if choice == "q":
        if self.active_menu.prev_menu is None:
          print2("Goodbye! ;)")
          return
        self.active_menu = self.active_menu.prev_menu
        continue
      choice = int(choice) - 1 # -1 to match 0-based indexing
      if isinstance(self.active_menu.options[choice].action, Menu):
        self.active_menu = self.active_menu.options[choice].action
      elif hasattr(self.active_menu.options[choice].action, "__call__"):
        self.active_menu.options[choice].action.__call__()
        any_key_to_continue()
    return

  def add_option(self, *args):
    """
    Can be used to dynamically add an option to the current menu. There are two
    supported ways to call this method. The first involves passing an already-
    constructed Option as the argument. The second involves passing arguments
    that will be passed to the Option constructor.

    Inputs:
      *args: Either one Option or 'name, action, flags' (the construction
             arguments for Option)
    """
    if len(args) == 2 or len(args) == 3:
      _opt = Option(*args)
    elif len(args) == 1 and isinstance(args[0], Option):
      _opt = args[0]
    if isinstance(_opt.action, Menu):
      _opt.action.prev_menu = self.active_menu
    elif not hasattr(_opt.action, "__call__"):
      raise TypeError("The action of each option must either be a Menu or "\
                        "be __call__-able.")
    self.options.append(_opt)
