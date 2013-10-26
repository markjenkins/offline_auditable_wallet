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

from os import urandom

from menu import run_menu, do_menu_run, always_return_false

KEY_SIZE = 256//8

def make_key_from_OS():
    return urandom(KEY_SIZE)

def make_key_from_dice_rolls():
    pass

def make_key_from_hex_string():
    pass

def run_key_gen_menu():
    key = do_menu_run(
        "We need some random data for this.\n"
        "Do you trust the crypto grade (R)andom number generator from your "
        "operating system? (/dev/urandom on Unix-like systems, "
        "CryptGenRandom() on Windows)\n"
        "As an alternative, do you want to provide some six sided (D)ice "
        "rolls or provide 32 random bytes from quality random source you trust "
        "in (H)ex? "
        "You can also (E)xit.",
        "R/D/H/E",
        { 'R': make_key_from_OS,
          'D': make_key_from_dice_rolls,
          'H': make_key_from_hex_string,
          'E': always_return_false,
          }
        )
    if isinstance(key, bytes):
        return key

def run_seed_gen_menu():
    pass

def run_passphrase_menu():
    pass

def generate_key_menu():
    key = run_menu(
        "How do you want to generate your key?\n"
        "Do you want to randomly generate a private (K)ey and print it, "
        "randomly generate a (S)eed, supply a (P)assphrase, "
        "or E(xit) to the main menu?",
        "K/S/P/E",
        { 'K': run_key_gen_menu,
          'S': run_seed_gen_menu,
          'P': run_passphrase_menu,
          'E': always_return_false, },
        )

if __name__ == "__main__":
    generate_key_menu()
