"""
This examples showcases how to use the built-in features to back-track and
go up menus. It also shows how you can implement an "Exit" option anywhere
within the menu which we do from within the deepest menu

For this example, the menu has the following layout:

 | 1. Go to Level 1 Menu [flags=0]
 |     >---| 1. Go to Level 2 Menu [flags=0]
 |         |     >---| 1. Go to Level 3 Menu [flags=0]       
 |         |         |     >---| 1. Quit Program [flags=0]   
 |         |         |         | 2. Go to main menu [flags=0]
 |         |         |
 |         |         | 2. Go up 1 level [flags=0]
 |         |         | 3. Go up 2 levels [flags=0]
 |         |
 |         | 2. Go up 1 level [flags=0]
 |
 | 2. Display menu mapping [flags=0]

"""
from py_menu import Option, Menu

splash = """\
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
           ~!~ Go back feature examples! ~!~            
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
main_menu = Menu(header="Main menu, pick an option!", 
                 splash=splash, 
                 on_quit_message="Custom quit message")

level1_menu = Menu("Level 1 Menu")
main_menu.add_option(f"Go to {level1_menu.header}", level1_menu)
main_menu.add_option("Display menu mapping", lambda: print(main_menu.pretty_menu()))

level2_menu = Menu("Level 2 Menu")
level1_menu.add_option(f"Go to {level2_menu.header}", level2_menu)
level1_menu.add_option("Go up 1 level", -1)

level3_menu = Menu("Level 3 Menu")
level3_menu.add_option("Quit Program", 0)
level3_menu.add_option("Go to main menu", 1)

level2_menu.add_option(f"Go to {level3_menu.header}", level3_menu)
level2_menu.add_option("Go up 1 level", -1)
level2_menu.add_option("Go up 2 levels", -2)


main_menu.mainloop()