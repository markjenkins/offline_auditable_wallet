#!/usr/bin/env python3

from oaw.bip39 import Bip39ChecksumError, bip39_words_to_bytes

try:
    bip39_words_to_bytes(input().strip())
except Bip39ChecksumError:
    exit(1)
else:
    exit(0)
