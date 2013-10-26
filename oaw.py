#!/usr/bin/env python3
# Python 3 only, does not have backwards compatible support for Python 2

# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from menu import run_menu, always_return_false, missing_menu_item

try:
    from key_generation import generate_key_menu
except ImportError:
    generate_key_menu = missing_menu_item
    
try:
    from key_restoration import restore_key_menu
except ImportError:
    restore_key_menu = missing_menu_item

def main_menu():
    run_menu( "Do you want to (G)enerate a private key, (R)estore a "
              "private key or Q(uit)?",
              "G/R/Q",
              { 'G': generate_key_menu,
                'R': restore_key_menu,
                'Q': always_return_false,
                }
              )

if __name__ == "__main__":
    main_menu()
