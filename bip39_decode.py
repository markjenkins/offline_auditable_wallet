from oaw.bip39 import bip39_words_to_bytes, bip39_checksum_calc

input_bytes = bip39_words_to_bytes(input().strip())
print(input_bytes.hex())
print("checksum " + bip39_checksum_calc(input_bytes))
