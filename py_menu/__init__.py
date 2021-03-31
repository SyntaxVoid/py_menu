""" Implements Menu and Option class """

import os
import platform
import sys
import subprocess
import textwrap


getch = input # default, overwrite it below if possible.
try:                           # msvrct.getch is exclusive to windows, but
  from msvcrt import getch     # its effects can be emulated in *nix. If
except ImportError:            # there are any problems setting getch, it
  try:                         # will default to 'input'.
    import tty
    import termios
    def getch(): # pylint: disable=function-redefined
      """ Will get one character from user without displaying it """
      file_desc = sys.stdin.fileno()
      old_attr = termios.tcgetattr(file_desc)
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
    original_lines = obj.split("\n")
    output_lines = []
    for line in original_lines:
      if line == "":
        output_lines += [""]
      else:
        output_lines += textwrap.wrap(line, width=n-spaces)
    to_print = " "*spaces + ("\n" + " "*spaces).join(output_lines)
    if obj.endswith("\n"):
      to_print += "\n"
    print(to_print, end=sep if m != len(s) else "", file=file, flush=flush)
  print(end=end)
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
  
  """
  The following can be used in place of the 'action' parameter when 
  constructing an Option. A Menu instance can (read: should) use these to 
  control how the Menu responds when the user uses these actions.
  
  The word "should" is used because it is up to the Menu class (or subclass)
  to implement these behaviors.
  """
  GO_TO_MAIN = 1 # Should go to the main menu
  EXIT = 0 # Should exit the menu loop
  GO_UP1 = -1 # Should go up 1 menu
  GO_UP2 = -2 # Should go up 2 menus
  GO_UP3 = -3 # Should go up 3 menus
  GO_UP4 = -4 # Should go up 4 menus
  GO_UP5 = -5 # Should go up 5 menus
  GO_UP6 = -6 # If you've gotten to this point, I'm a little scared...
  # Pass any other negative number as 'action' to go up that many menus

  def __init__(self, name, action, pause_after_completion=True, flags=0):
    """
    Initializes an Option object. This will be displayed by Menu.

    Inputs:
      name: str - The name of the option. This will be displayed
      action: callable, Menu, or int - The action to take when this option is
              selected. If it is a callable, it will be __call__-ed. If it is a
              Menu object, control will be transfered to this Menu and whatever
              the current Menu was will be set as the previous menu. If it is
              1, the program should return to the toplevel menu. If it is 0, it 
              will quit the menu loop entirely.If it is a negative integer, the
              Menu should try to go up that many menus.
              
              Having the __call__-able object return the literal string "break"
              will cause the menu to exit.

              These are implementation features of Menu/its subclasses
      
      pause_after_completion: bool - Whether or not to pause after an action
                              has been completed
      flags: Not implemented for the base Option and Menu classes. The
             definition of flags can be set by whoever inherits from Option
             or Menu.
    """
    self.name = name
    # We only want to accept an action if *any* of the following are true:
    #   1. action is callable
    #   2. action is a Menu or a subclass of Menu
    #   3. action is a non-positive integer
    if (  hasattr(action, "__call__") \
        or isinstance(action, Menu) \
        or (isinstance(action, int) and action <= 1)):
      self.action = action
    else:
      raise TypeError("Action must either be callable, a Menu instance, or a "\
                     +"non-positive integer!")
    self.flags = flags
    self.pause_after_completion = pause_after_completion
    return
  
  def __str__(self):
    return f"{self.name}"


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
  DEFAULT_OPTION_CLASS = Option
  def __init__(self, header, options=None, splash="", 
               on_quit_message="", show_quit_at_toplevel=True):
    """
    Initializer for Menu objects. Provides an easily adaptable framework for
    creating command-line-interface menus.

    Inputs:
      header: str - The message to be displayed at the top of the menu.
      options: [Option] - A list of Option objects to be displayed.
      splash: str - A single message to display when mainloop begins. For
              nested Menu objects, the splash message will ONLY be printed
              for the initial object that calls mainloop.
      on_quit_message: str - A message to display when the user quits from the
                       toplevel menu. Setting this for a non-toplevel menu has
                       no effect.
      show_quit_at_toplevel: bool - Whether or not to display a "Quit Program"
                             option at the toplevel menu.
    """
    self.header = header
    self.active_menu = self
    self.prev_menu = None
    self.options = [] # This gets populated within add_option in the for loop
    options = [] if options is None else options
    for option in options:
      self.add_option(option) # This is where self.options is built
    self.splash = splash
    self._splash_shown = False # True if splash has been shown. False otherwise
    self.on_quit_message = on_quit_message
    self.show_quit_at_toplevel = show_quit_at_toplevel
    try:
      self.flag_descriptions = self.DEFAULT_OPTION_CLASS.FLAG_DESCRIPTIONS
    except:
      self.flag_descriptions = ""
    return

  def __str__(self):
    out = ""
    out += self.active_menu.header + "\n"
    opt_str = "    {option_num:2d}. {option_name}\n"
    q_str = "     q. {msg}\n"
    for option_num, option in enumerate(self.active_menu.options, start=1):
      out += opt_str.format(option_num=option_num, option_name=option.name)
    if self.active_menu.prev_menu is None:
      if self.show_quit_at_toplevel: # Don't merge these two ifs!^
        out += q_str.format(msg="Quit program")
    else:
      out += q_str.format(msg="Previous menu")
    return out

  @property
  def valid_options(self):
    out = []
    for i in range(len(self.active_menu.options)):
      out.append(str(i+1))
    if self.active_menu.prev_menu is None:
      if self.show_quit_at_toplevel:
        out.append("q")
    else:
      out.append("q")
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
      # Handle the special "q" cases
      if choice == "q":
        if self.active_menu.prev_menu is None: # If at the top-level
          print2(self.on_quit_message)
          return
        self.active_menu = self.active_menu.prev_menu
        continue
      choice = int(choice) - 1 # -1 to match 0-based indexing
      
      # Handle the special Option.EXIT case
      action = self.get_action(choice)
      if action == Option.EXIT:
        print2(self.on_quit_message)
        return
      
      # Handle the special Option.GO_TO_MAIN case.
      if isinstance(action, int) and action == Option.GO_TO_MAIN:
        while self.active_menu.prev_menu is not None:
          self.active_menu = self.active_menu.prev_menu


      # Handle the special Option.GO_UPn cases. Will try to go up as many
      # levels as requested. If the toplevel menu is reached, it will 
      # stop trying to go up levels and will remain at the toplevel.
      if isinstance(action, int) and action < 0:
        for _level in range(-action):
          if self.active_menu.prev_menu is not None: # If not toplevel
            self.active_menu = self.active_menu.prev_menu
          else:
            break

      if isinstance(action, Menu):
        self.active_menu = action
      elif hasattr(action, "__call__"):
        try:
          result = action.__call__()
          if result == "break":
            # When a method returns 'break', we should exit the menu
            return
        except KeyboardInterrupt:
          print2("\nAction was aborted by the user")
        else:
          if isinstance(result, str) and result.lower() == "q": 
            continue
        if self.get_option(choice).pause_after_completion:
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
    if len(args) in (2,3,4):
      # pylint: disable=no-value-for-parameter
      _opt = self.DEFAULT_OPTION_CLASS(*args) 
    elif len(args) == 1 and isinstance(args[0], self.DEFAULT_OPTION_CLASS):
      _opt = args[0]
    else:
      raise TypeError("The option must be arguments for the option "\
                     f"constructor or of type '{self.DEFAULT_OPTION_CLASS}'.")
    if isinstance(_opt.action, Menu):
      _opt.action.prev_menu = self.active_menu
    self.options.append(_opt)

  def pretty_menu(self, indent_level=0, __menu_cache=None):
    """ 
    Creates a pretty version of the menu. Catches and handles circular menu
    dependencies before they become a problem.
    """
    __menu_cache = [] if __menu_cache is None else __menu_cache
    out = ""
    base = " |"
    level = "         |"
    for n, option in enumerate(self.options, start=1):
      if n == 1 and indent_level != 0:
        start = base + level*(indent_level - 1) + "     "
        out += start + ">---|" + f"{n:2d}. {str(option)}\n"
      else:
        start = base + level*(indent_level)
        out += start + f"{n:2d}. {str(option)}\n"
      if isinstance(option.action, Menu) and option.action not in __menu_cache:
        __menu_cache.append(option.action)
        out += option.action.pretty_menu(indent_level+1, __menu_cache)  
    if indent_level == 1:
      out += base + "\n"
    elif indent_level == 0:
      if self.flag_descriptions:
        out += "\n --- Flag Descriptions (Can be added together) ---\n"
        out += self.flag_descriptions
    else:
      start = base + level*(indent_level - 1) + "     "
      out += start + "\n"
    return out

  def get_option(self, choice):
    """
    Returns the option for the given choice. If the choice is invalid, will
    either raise TypeError (choice is not an int) or IndexError (out of range).
    """
    return self.active_menu.options[choice]

  def get_action(self, choice):
    """
    Returns the action for the given choice. If choice is invalid, will either
    raise TypeError (choice is not an int) or IndexError (out of range).
    """
    return self.get_option(choice).action

  