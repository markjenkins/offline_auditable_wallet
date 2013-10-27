# Copyright Mark Jenkins, 2013
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved. This file is offered as-is,
# without any warranty.
# http://www.gnu.org/prep/maintain/html_node/License-Notices-for-Other-Files.html
# @author Mark Jenkins <mark@markjenkins.ca>


# python imports
from itertools import takewhile, chain
from functools import reduce
from sys import version_info

from ecdsa.util import number_to_string

# some algorithmic inspiration from
# https://bitcointalk.org/index.php?topic=1026.0
# but without explicit exponentiation, all multiplies and divides

BITS_PER_BYTE = 8

def int_to_minimal_bytes(number):
    return number_to_string(number, number)

if version_info[0] >= 3 and version_info[1] >= 2:
    # using int.from_bytes functions built in to
    # python 3.2 and later is best
    def bytes_to_int(bytesies):
        return int.from_bytes(bytesies, 'big')

    def int_to_bytes(number, length=None):
        # if length is None, create a number of the same order
        # if length is specified in bytes, set order to the biggest int of
        return ( int_to_minimal_bytes(number) if length == None
                 else number.to_bytes(length, 'big') )

    # which is too bad, I really liked my implementation of bytes_to_int
    # Hopefully the underlying implementation also only does OR and shifts
    # def bytes_to_int(bytesies):
    # return reduce(
    #    lambda accumulation, single_byte:
    #        accumulation<<BITS_PER_BYTE | single_byte,
    #    bytesies,
    #    0 )
else:
    # but alas, might as well use python-ecdsa's functions
    from ecdsa.util import string_to_number as bytes_to_int
    def int_to_bytes(number, length=None):
        # if length is None, create a number of the same order
        # if length is specified in bytes, set order to the biggest int of
        return ( int_to_minimal_bytes(number) if length == None
                 else number_to_string(number, 2
                                       ** (length*BITS_PER_BYTE) -1) )

# there has got to be something built in for this, no?
def repeat_transform_until(transform, value, predicate):
    while predicate(value):
        value = transform(value)
        yield value

def big_integer_to_dict_keys(big_int, num_symbols):
    # does this terminate in the right place?
    return reversed(list(
        small_int
        for ignore, small_int in 
        repeat_transform_until(
            lambda values: divmod(values[0], num_symbols),
            (big_int, 0),
            lambda values: values[0] != 0
            )
        ))

def big_integer_to_dictionary_iter(big_int, dictionary):
    return (
        dictionary[small_int]
        for small_int in big_integer_to_dict_keys(
            big_int, len(dictionary))
        )

def sym_encode(bytesies, dictionary):
    return big_integer_to_dictionary_iter(
        bytes_to_int(bytesies), dictionary )

def sym_encode_with_zero_pad(bytesies, dictionary):
    # pad with the first dictionary word for any zeros
    symbols_for_zero = tuple(
        dictionary[0]
        for i in takewhile(lambda x: x == 0, bytesies) )
    return chain( 
        symbols_for_zero,
        sym_encode(bytesies, dictionary)
        ) # return expression

def sym_decode(syms, reverse_dictionary, length=None):
    num_symbols = len(reverse_dictionary)
    return int_to_bytes(
        reduce( lambda accumulation, symbol:
                       accumulation*num_symbols+reverse_dictionary[symbol],
                syms, 0),
        length)

def sym_decode_with_zero_pad(syms, reverse_dictionary):
    # important, we don't want to involve any leading zeros twice
    syms_buffer = tuple(syms)
    leading_zeros = bytes(
        0
        for i in takewhile( lambda x: reverse_dictionary[x] == 0,
                            syms_buffer)
        )

    # if there is more then just zeros, return the leading zeros plus everything
    # else decoded
    if len(leading_zeros) != len(syms_buffer):
        return leading_zeros + sym_decode(syms_buffer, reverse_dictionary, None)
    # else everyting was zeros
    else:
        return leading_zeros

def create_reverse_dictionary(dictionary):
     return dict( (sym, i)
                  for i, sym in enumerate(dictionary) )
