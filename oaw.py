#!/usr/bin/python3
# Python 3 only, does not have backwards compatible support for Python 2

# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from menu import run_menu, run_breakable_menu, always_return_false
from key_generation import generate_key_menu
from key_restoration import restore_key_menu

def main_menu():
    while True:
        run_menu( "Do you want to (G)enerate a private key, (R)estore a "
                  "private key or Q(uit)?",
                  "G/R/Q",
                  { 'G': generate_key_menu,
                    'R': restore_key_menu,
                    'Q': exit,
                    }
                  )

if __name__ == "__main__":
    main_menu()
