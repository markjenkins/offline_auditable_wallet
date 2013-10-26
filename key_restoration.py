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

from menu import run_menu, always_return_false

def restore_xor_scheme_key_menu():
    pass

def restore_key_from_seed_menu():
    pass

def restore_key_from_passphrase_menu():
    pass

def restore_key_menu():
    run_menu(
        "Is your key encoded with a 2 of 3 (X)or scheme, "
        "generated from a (S)eed, "
        "derived from a (P)assphrase or "
        "(E)xit to the main menu?",
        ( ('X', restore_xor_scheme_key_menu),
          ('S', restore_key_from_seed_menu),
          ('P', restore_key_from_passphrase_menu),
          ('E', always_return_false),
          )
        )

if __name__ == "__main__":
    restore_key_menu()
