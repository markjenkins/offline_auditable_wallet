# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from math import log

from .encoding import (
    create_reverse_dictionary, sym_decode
    )
from .key_from_random import make_key_building_from_existing_bytes_plus_urandom

DICTIONARY = tuple( str(i) for i in range(1, 6+1) )
REVERSE_DICTIONARY = create_reverse_dictionary(DICTIONARY)

def dice_decode(v, length=None):
    dice_buffer = tuple(v)
    return sym_decode(dice_buffer, REVERSE_DICTIONARY, length)

def break_up_dice_input_string(input_string):
    # assumption for anyone modding this from the original six sided dice
    # code, each dice roll is one digit
    return (character for character in input_string
            if character in DICTIONARY )

def get_safe_number_of_bytes_from_dice_rolls(dice_rolls):
    dice_buffer = tuple(dice_rolls)
    length = int( (log(len(DICTIONARY), 2) * len(dice_buffer)) // 8 )    
    return dice_decode(dice_buffer, length+1)[:length]

def return_byte_decoded_dice_from_prompt():
    return_bytes = get_safe_number_of_bytes_from_dice_rolls(
        break_up_dice_input_string(
            input("input your dice rolls\n"
                 "(2.5 bits of entropy each)> ") )
        )
    print( "thanks, got %s bits (%s bytes) out of that " %
           (len(return_bytes)*8, len(return_bytes) ) )
    print()
    return return_bytes

def make_key_from_dice_rolls_provided(dice_rolls):
    return make_key_building_from_existing_bytes_plus_urandom(
        get_safe_number_of_bytes_from_dice_rolls(dice_rolls) )

def make_key_from_dice_rolls_prompt():
    return make_key_building_from_existing_bytes_plus_urandom(
        return_byte_decoded_dice_from_prompt() )
