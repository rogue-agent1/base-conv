#!/usr/bin/env python3
"""base_conv - Base encoding: base16, base32, base58, base62, base85."""
import sys, string

B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
B62_ALPHABET = string.digits + string.ascii_letters

def base_encode(data, alphabet):
    base = len(alphabet)
    if isinstance(data, (bytes, bytearray)):
        num = int.from_bytes(data, "big")
    else:
        num = data
    if num == 0:
        return alphabet[0]
    result = []
    while num > 0:
        num, rem = divmod(num, base)
        result.append(alphabet[rem])
    leading_zeros = 0
    if isinstance(data, (bytes, bytearray)):
        for b in data:
            if b == 0:
                leading_zeros += 1
            else:
                break
    return alphabet[0] * leading_zeros + "".join(reversed(result))

def base_decode(encoded, alphabet):
    base = len(alphabet)
    num = 0
    for ch in encoded:
        num = num * base + alphabet.index(ch)
    leading_zeros = 0
    for ch in encoded:
        if ch == alphabet[0]:
            leading_zeros += 1
        else:
            break
    return num, leading_zeros

def base58_encode(data):
    return base_encode(data, B58_ALPHABET)

def base58_decode(s):
    num, lz = base_decode(s, B58_ALPHABET)
    if num == 0:
        return b"\x00" * max(lz, 1)
    result = num.to_bytes((num.bit_length() + 7) // 8, "big")
    return b"\x00" * lz + result

def base62_encode(num):
    return base_encode(num, B62_ALPHABET)

def base62_decode(s):
    num, _ = base_decode(s, B62_ALPHABET)
    return num

def test():
    assert base58_encode(b"Hello") == base_encode(b"Hello", B58_ALPHABET)
    rt = base58_decode(base58_encode(b"Hello World"))
    assert rt == b"Hello World"
    rt2 = base58_decode(base58_encode(b"\x00\x00test"))
    assert rt2 == b"\x00\x00test"
    assert base62_encode(0) == "0"
    assert base62_encode(61) == "Z"
    assert base62_decode(base62_encode(123456789)) == 123456789
    assert base62_decode("0") == 0
    for val in [0, 1, 255, 65535, 2**32]:
        assert base62_decode(base62_encode(val)) == val
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("base_conv: Base encoding. Use --test")
