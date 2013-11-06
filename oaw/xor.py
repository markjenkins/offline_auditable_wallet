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

from .entropy import get_entropy_source_menu
from .rfc_1760_dict_encode import joined_words_for_bytes

def restore_xor_scheme_key_menu():
    pass

def xor_bytes(bytes1, bytes2):
    return bytes( b1 ^ b2 for b1, b2 in zip(bytes1, bytes2) )

DISPLAY_XOR_FIRST_PROMPT = \
    "Hit enter when you're ready for the first xor component> "
DISPLAY_COMPONENT_NUMBER_FMT = "component %s"
NEXT_XOR_PROMPT = "hit enter when you're ready for the next xor component> "
LAST_XOR_PROMPT = "last one. Hit enter to clear> "

def display_xor_components_with_shell_clear(components):
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
    input("Hit enter when you're ready for the first xor component> ")

    components = tuple(components) # buffer
    if os.name == 'nt':
        display_xor_components_with_shell_clear(components)
    else:
        import curses
        # still a work in progress
        # curses.wrapper(display_xor_components_curses, components)
        display_xor_components_with_shell_clear(components)

def display_xor_components_curses(stdscr, components):
    import curses
    stdscr.erase()
    
    for i, comp in enumerate(components, 1): 
        stdscr.insstr(DISPLAY_COMPONENT_NUMBER_FMT % i)
        stdscr.insstr(comp)
        if i < len(components):
            stdscr.insstr(NEXT_XOR_PROMPT)
        else:
            stdscr.insstr(LAST_XOR_PROMPT)
        stdscr.getch()

        stdscr.erase()
    
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

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
    assert(len(originals) == 3)
    pieces_matrix = tuple( tuple(break_into_n(stream, 3))
                           for stream in originals )
    return (
        b''.join(row)
        for row in 
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
