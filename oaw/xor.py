# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

import os
from os import urandom
from textwrap import fill

from .entropy import get_entropy_source_menu
from .rfc_1760_dict_encode import (
    joined_words_for_bytes, words_string_to_32_bytes,
    )

NUM_PARTS = 3

def part_joiner(parts):
   return (
        b''.join(row)
        for row in parts )  

def xor_rfc1760_to_private_key(args):
    # only support breaking into three parts for now..
    if len(args) != NUM_PARTS:
        raise Exception(
            "You must provide three parts, one can be blank")

    # convert each of the inputs to 32 bytes, for a blank input,
    # use all zeros
    parts = tuple(words_string_to_32_bytes(a) if a != ''
                  else None
                  for a in args )
    # replace the part that is None with a xor of the other two
    parts = tuple(
        xor_bytes(parts[(i+1)%NUM_PARTS], parts[(i-1)%NUM_PARTS])
        if part == None else part
        for i, part in enumerate(parts)
        )    

    restored_sub_parts = tuple(
        tuple(break_into_n(b, NUM_PARTS))
        for b in parts
        )
    # we really only need to restore part one...
    restored_parts = tuple(part_joiner( (
                (restored_sub_parts[0][0],
                 restored_sub_parts[1][1],
                 restored_sub_parts[2][2],
                 ),
                (restored_sub_parts[1][0],
                 restored_sub_parts[2][1],
                 restored_sub_parts[0][2],
                 ),
                (restored_sub_parts[2][0],
                 restored_sub_parts[0][1],
                 restored_sub_parts[1][2],
                 ),
                ) ) )
    # but we do get to do this sanity check
    for i in range(NUM_PARTS):
        assert(restored_parts[i] ==
               xor_bytes(restored_parts[(i+1)%NUM_PARTS],
                         restored_parts[(i-1)%NUM_PARTS] ) )

    return restored_parts[0], True

def restore_xor_scheme_key_menu():
    pass

def xor_bytes(bytes1, bytes2):
    return bytes( b1 ^ b2 for b1, b2 in zip(bytes1, bytes2) )

DISPLAY_XOR_FIRST_PROMPT = \
    "Hit enter when you're ready for the first xor component> "
DISPLAY_COMPONENT_NUMBER_FMT = "component %s"
NEXT_XOR_PROMPT = "hit enter when you're ready for the next xor component> "
LAST_XOR_PROMPT = "last one. Hit enter to clear> "
READY_PROMPT = "ready for the next component? Hit enter. > "

def display_xor_components_with_shell_clear(components):
    input("Hit enter when you're ready for the first xor component> ")

    for i, comp in enumerate(components, 1): 
        print(DISPLAY_COMPONENT_NUMBER_FMT % i)
        print(comp)
        if i < len(components):
            input(NEXT_XOR_PROMPT)
        else:
            input(LAST_XOR_PROMPT)

        if os.name == 'nt':
            # haven't actually tested this on Windows
            os.system('cls')
        else:
            os.system('clear')

def display_xor_components(components):
    components = tuple(components) # buffer
    if os.name == 'nt':
        display_xor_components_with_shell_clear(components)
    else:
        import curses
        curses.wrapper(display_xor_components_curses, components)

def display_xor_components_curses(stdscr, components):
    import curses
    stdscr.erase()
    
    def fill_window(msg):
       stdscr.addstr(fill(msg, curses.COLS))

    def fill_window_w_newline(msg=""):
       stdscr.addstr(fill(msg, curses.COLS)+"\n")

    for i, comp in enumerate(components, 1): 
        fill_window_w_newline(DISPLAY_COMPONENT_NUMBER_FMT % i)
        fill_window(READY_PROMPT)
        stdscr.refresh()
        stdscr.getch()
        stdscr.addstr("\n")

        fill_window_w_newline(comp)
        if i < len(components):
            fill_window(NEXT_XOR_PROMPT)
        else:
            fill_window(LAST_XOR_PROMPT)
        stdscr.refresh()

        stdscr.getch()

        stdscr.erase()
    
def break_into_n(bytesies, n):
    length = len(bytesies)
    part_size = length//n
    last_part_end = part_size * n
    return (
        bytesies[i:j] if j != last_part_end else bytesies[i:]
        for i, j in zip( range(0, length, part_size),
                         range(part_size, length+1, part_size) )
        )

def create_2_of_3_xor_stripes(originals):
    for o in originals[1:]:
        assert( len(o) == len(originals[0]) )
    
    # I'm too lazy to write this generic and careful right now
    # not even sure a more generic version is useful
    assert(len(originals) == NUM_PARTS)
    pieces_matrix = tuple( tuple(break_into_n(stream, NUM_PARTS))
                           for stream in originals )
    return part_joiner(
        ( (pieces_matrix[0][0], pieces_matrix[2][1], pieces_matrix[1][2]),
          (pieces_matrix[1][0], pieces_matrix[0][1], pieces_matrix[2][2]),
          (pieces_matrix[2][0], pieces_matrix[1][1], pieces_matrix[0][2]) )
        )

def show_wallet_xor_scheme(private_key_bytes, compressed):
    entropy_source = get_entropy_source_menu()
    if entropy_source is False:
        return False
    if entropy_source == None:
        entropy_source = urandom
    random_bytes = entropy_source(len(private_key_bytes))
    rand_xor = xor_bytes(private_key_bytes, random_bytes)

    stripes = create_2_of_3_xor_stripes(
        (private_key_bytes, random_bytes, rand_xor) )

    # important to buffer this so we can iterate through it again
    # down below
    stripes = tuple(stripes)
    for stripe in stripes:
        assert( len(stripe) == len(private_key_bytes) )

    display_xor_components( joined_words_for_bytes(b)
                            for b in stripes )

    return False
