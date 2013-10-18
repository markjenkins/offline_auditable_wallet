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

def run_key_gen_menu():
    pass

def run_seed_gen_menu():
    pass

def run_passphrase_menu():
    pass

def generate_key_menu():
    run_breakable_menu(
        "How do you want to generate your key?\n"
        "Do you want to randomly generate a private (K)ey and print it "
        "randomly generate a (S)eed, supply a (P)assphrase, "
        "or E(xit) to the main menu?",
        "K/S/P/E",
        { 'R': run_key_gen_menu,
          'S': run_seed_gen_menu,
          'P': run_passphrase_menu,
          'E': always_return_false, },
        )

def restore_xor_scheme_key_menu():
    pass

def restore_key_from_seed_menu():
    pass

def restore_key_from_passphrase_menu():
    pass

def restore_key_menu():
    run_breakable_menu(
        "Is your key encoded with a 2 of 3 (X)or scheme, "
        "generated from a (S)eed, "
        "derived from a (P)assphrase or "
        "(E)xit to the main menu?",
        "X/S/P/E",
        { 'X': restore_xor_scheme_key_menu,
          'S': restore_key_from_seed_menu,
          'P': restore_key_from_passphrase_menu,
          'E': always_return_false, },
        )

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
