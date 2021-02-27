#!/usr/bin/env python3

from secrets import token_bytes
from sys import argv

from oaw.bip39 import bytes_to_bip39_w_checksum

size_bits = 128
if len(argv)>1:
    size_bits = int(argv[1])

print(bytes_to_bip39_w_checksum(token_bytes(size_bits//8)))
