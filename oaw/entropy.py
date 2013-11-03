# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from .menu import do_menu_run, always_return_false

def return_none(*args, **kargs): pass

try:
    from .hex import make_entropy_source_from_hex_prompt
except ImportError:
    make_entropy_source_from_hex_prompt = return_none

try:
    from .dice import make_entropy_source_from_dice_rolls_prompt
except:
    make_entropy_source_from_dice_rolls_prompt = return_none

def get_entropy_source_menu():
    return do_menu_run(
        "We need some random data for this.\n"
        "Do you fully trust the crypto grade (R)andom number generator from "
        "your operating system? (/dev/urandom on Unix-like systems, "
        "CryptGenRandom() on Windows)\n"
        "Or, would you like to supplement it with some entropy of your own "
        "by rolling some six sided (D)ice or "
        "provide bytes from whatever other random source you "
        "trust in (H)ex? "
        "You can also (E)xit.",
        ( ('R', return_none),
          ('D', make_entropy_source_from_dice_rolls_prompt),
          ('H', make_entropy_source_from_hex_prompt),
          ('E', always_return_false),
          )
        )
   
