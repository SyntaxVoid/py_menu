"""
This example showcases how it's possible to define your own exit logic. If any
action returns the literal string "break", the program will exit the menu. This
could be useful if you need options like "Save and quit" or "Discard and quit"
"""
import time

from py_menu import Menu, Option

def save_and_quit():
  print("Now saving data...")
  time.sleep(2)
  print("Data saved!")
  return "break"

def discard_and_quit():
  print("Discarding data!")
  return "break"


splash = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              ~!~ Custom Exit Example ~!~               
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# We disable the built-in quit option by setting show_quit_at_toplevel to False
main_menu = Menu("Main Menu - Pick an Option!",
                 splash=splash,
                 show_quit_at_toplevel=False)
main_menu.add_option("Save and quit", save_and_quit)
main_menu.add_option("Discard and quit", discard_and_quit)

main_menu.mainloop()
