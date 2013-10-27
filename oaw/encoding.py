# python imports
from itertools import takewhile, chain
from functools import reduce
from sys import version_info

from ecdsa.util import number_to_string

# some algorithmic inspiration from
# https://bitcointalk.org/index.php?topic=1026.0
# but without explicit exponentiation, all multiplies and divides

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
    # BITS_PER_BYTE = 8
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
                 else number_to_string(number, 2 ** (length*8) -1) )



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

def sym_decode(syms, reverse_dictionary, length):
    num_symbols = len(reverse_dictionary)
    return int_to_bytes(
        reduce( lambda accumulation, symbol:
                       accumulation*num_symbols+reverse_dictionary[symbol],
                syms, 0),
        length)

def create_reverse_dictionary(dictionary):
     return dict( (sym, i)
                  for i, sym in enumerate(dictionary) )
