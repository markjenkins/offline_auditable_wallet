#!/usr/bin/env python3
# Python 3 only, does not have backwards compatible support for Python 2

# Copyright Mark Jenkins, 2017
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from os.path import dirname, join as path_join

from .elevenbitdictencode import (
    BITS_PER_WORD, BITS_PER_BYTE, DICTIONARY_SIZE,
    numbers_to_words, bytes_to_words, mask_first_n_bits, words_to_bytes,
    test_11bit_dict_encode, bytes_to_words as bytes_to_eleven_bit_words
) # end import

dictionary_path = path_join(dirname(__file__), "bip39english.txt" )
with open(dictionary_path) as f:
    DICTIONARY = tuple( line.strip() for line in f )

assert( len(DICTIONARY) == DICTIONARY_SIZE )

WORD_TO_NUMBER = dict( (word, i) for i, word in enumerate(DICTIONARY) )

def bytes_to_words(input_bytes):
    number_of_bits = input_bytes*BITS_PER_BYTE
    missing_bits_count = (0 if number_of_bits % 11 == 0 else 
                      ((number_of_bits //11)+1)*11 - number_of_bits )
    input_bytes_hashed = sha256(input_bytes).digest()
    return bytes_to_eleven_bit_words(
        input_bytes, DICTIONARY, 
        padding=input_bytes_hashed[:missing_bits_count//8])
