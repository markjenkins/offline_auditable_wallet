#!/usr/bin/env python3
# Python 3 only, does not have backwards compatible support for Python 2

# Copyright Mark Jenkins, 2013, 2017
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>

from itertools import islice
from functools import reduce

BITS_PER_WORD = 11
BITS_PER_BYTE = 8

DICTIONARY_SIZE = 2**BITS_PER_WORD

# more coding work to be able to work outside these contraints
assert( (BITS_PER_BYTE * 2) > BITS_PER_WORD )
assert( BITS_PER_BYTE < BITS_PER_WORD )

def mask_first_n_bits(n):
    return sum( 1<<i for i in range(n) )

# combinations of bits sources we cycle through adding up to 11
# (8,3)
# (5,6)
# (2,8, hold)
# (2,8,1)
# (1,8, hold)
# (1,8,2)
# (0,8, hold)
# (8,3)
# ...

def reduction_of_bytes_to_word_numbers_glue_cases(a, new_bits):
    (output_bytes, previous_bits, previous_bits_count) = a
    
    # we're storing BITS_PER_BYTES total and using previous_bits_count
    # from previous_bits and all some or all of new_bits
    
    total_bits_to_be_used = min( BITS_PER_WORD,
                                 previous_bits_count + BITS_PER_BYTE)
    used_bits_from_new = total_bits_to_be_used - previous_bits_count
    assert( used_bits_from_new <= BITS_PER_BYTE )

    bit_glue_result = (previous_bits | (
            (new_bits & mask_first_n_bits(used_bits_from_new))
            << previous_bits_count) )

    return ( ( output_bytes,
               bit_glue_result,
               previous_bits_count+used_bits_from_new, )
             if total_bits_to_be_used < BITS_PER_WORD

             else ( output_bytes + (bit_glue_result,) ,
                    new_bits >> used_bits_from_new,
                    BITS_PER_BYTE - used_bits_from_new
                    ) # tuple
             ) # return ternary expression

def reduction_of_bytes_to_word_numbers(a, new_byte):
    (output_bytes, previous_bits, previous_bits_count) = a
    return (
        # the simple case is that there are no leftover bits and we just
        # shuffle the new byte down for the next call
        (output_bytes, new_byte, BITS_PER_BYTE)
        if previous_bits_count == 0

        # otherwise we have to glue previous_bits and some of new_byte together
        else reduction_of_bytes_to_word_numbers_glue_cases(
            (output_bytes, previous_bits, previous_bits_count), new_byte)
        ) # return ternary expression

def calc_extra_pad_bytes_required(bits_shortfall):
    return ( 0
             if bits_shortfall == 0
             else ( (bits_shortfall // BITS_PER_BYTE)+1 ) )

def bytes_to_word_numbers(bytes_msg, padding=None):
    bits_storage_required = len(bytes_msg)*BITS_PER_BYTE
    words_required = (
        (bits_storage_required // BITS_PER_WORD)
        if (bits_storage_required % BITS_PER_WORD) == 0
        else (bits_storage_required // BITS_PER_WORD) +1 )
    bits_shortfall = words_required * BITS_PER_WORD - bits_storage_required

    assert( (words_required*BITS_PER_WORD) >= bits_storage_required )

    extra_pad_bytes_required = calc_extra_pad_bytes_required(bits_shortfall)
    if padding == None:
        bytes_to_encode = bytes_msg + ( b'\x00' * extra_pad_bytes_required )
    else:
        assert(len(padding)>=extra_pad_bytes_required)
        bytes_to_encode = bytes_msg + padding[:extra_pad_bytes_required]

    # call reduction_of_bytes_to_word_numbers repeately with reduce()
    # the sequence we feed to reduce() (first argument) is the bytes 
    # we're encoding
    #
    # the initial state and state passed to all calls to
    # reduction_of_bytes_to_word_numbers() is a tuple consiting of
    #  [0] "output_bytes", a tuple of word numbers accumulated so far
    #                      initilized as an empty tuple
    #
    #  [1] "previous_bits" an integer representation of a byte (0<p<=255)
    #                      that will always contain leftover
    #                      unused bits from the last call to reduction_of_bytes..
    #                      in the initilization case this is just None because
    #                      there are unused bits fist, meaningful on the second
    #                      call of reduction_of_bytes
    #
    #  [2] "previous_bits_count" An integer counting the number of unused bits
    #                            that [1] previous_bits includes.
    #                            This is 0 in the initialization case.
    #
    # after reduce() returns, we extract the [0] element which has the
    # accumulated word numbers as a tuple
    return reduce( reduction_of_bytes_to_word_numbers,
                   bytes_to_encode, (() , None, 0) )[0]

def numbers_to_words(numbers_stream, dictionary):
    return ( dictionary[num] for num in numbers_stream )

def bytes_to_words(input_bytes, dictionary, padding=None):
    assert( len(dictionary) == DICTIONARY_SIZE )
    return numbers_to_words(bytes_to_word_numbers(input_bytes,
                                                  padding=padding),
                            dictionary
    ) # numbers_to_words


def new_bytes_from_bits(previous_bits, previous_bits_count, new_word_number):
    combined_bits = previous_bits | (new_word_number << previous_bits_count)
    bit_count = previous_bits_count + BITS_PER_WORD
    accum = b''
    while bit_count >= BITS_PER_BYTE:
        accum = accum + bytes(
            (combined_bits & mask_first_n_bits(BITS_PER_BYTE),) )
        combined_bits >>= BITS_PER_BYTE
        bit_count -= BITS_PER_BYTE
    return accum, combined_bits, bit_count

def reduction_of_word_numbers_to_bytes(a, new_word_number ):
    (bytes_accumulated, previous_bits, previous_bits_count) = a
    new_bytes, new_leftover_bits, new_leftover_bits_count = new_bytes_from_bits(
        previous_bits, previous_bits_count, new_word_number)

    return ( (bytes_accumulated + new_bytes, 
              new_leftover_bits,
              new_leftover_bits_count )
             )

def numbers_to_bytes(numbers_stream):
    # would be nice to not have to buffer this
    numbers_stream = tuple(numbers_stream)
    return ( numbers_stream if len(numbers_stream) == 1
            else reduce( reduction_of_word_numbers_to_bytes,
                         islice(numbers_stream, 1, len(numbers_stream) ),
                         (b'', numbers_stream[0], BITS_PER_WORD) )[0]
            ) # end tenary return expression

def words_to_numbers(words, word_to_number_dict):
    return( word_to_number_dict[word] for word in words )

def words_to_bytes(words, word_to_number_dict):
    return numbers_to_bytes(words_to_numbers(words, word_to_number_dict))

def test_11bit_dict_encode(dictionary, word_to_number_dict):
    from os import urandom
    number_of_bytes = 128//BITS_PER_BYTE
    random_bytes = urandom(number_of_bytes)
    word_list = tuple(bytes_to_words(random_bytes, dictionary))
    bytes_output = words_to_bytes(word_list, word_to_number_dict)
    assert( bytes_output == random_bytes )
    assert( tuple(bytes_to_words(bytes_output, dictionary)) == word_list )

    
