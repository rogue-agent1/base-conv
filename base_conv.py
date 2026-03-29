#!/usr/bin/env python3
"""base_conv: Base conversion (base16/32/58/62/64/85)."""
import string, sys

B58_ALPHA = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
B62_ALPHA = string.digits + string.ascii_letters
B85_ALPHA = "".join(chr(i) for i in range(33, 118))

def to_base(num, base, alphabet=None):
    if alphabet is None:
        alphabet = string.digits + string.ascii_lowercase
    if num == 0: return alphabet[0]
    result = []
    while num > 0:
        result.append(alphabet[num % base])
        num //= base
    return "".join(reversed(result))

def from_base(s, base, alphabet=None):
    if alphabet is None:
        alphabet = string.digits + string.ascii_lowercase
    lookup = {c: i for i, c in enumerate(alphabet)}
    result = 0
    for c in s:
        result = result * base + lookup[c]
    return result

def base58_encode(data: bytes) -> str:
    num = int.from_bytes(data, "big")
    encoded = to_base(num, 58, B58_ALPHA) if num > 0 else ""
    pad = 0
    for b in data:
        if b == 0: pad += 1
        else: break
    return B58_ALPHA[0] * pad + encoded

def base58_decode(s: str) -> bytes:
    pad = 0
    for c in s:
        if c == B58_ALPHA[0]: pad += 1
        else: break
    num = from_base(s[pad:], 58, B58_ALPHA) if s[pad:] else 0
    result = num.to_bytes((num.bit_length() + 7) // 8, "big") if num > 0 else b""
    return b"\x00" * pad + result

def test():
    # Base conversion
    assert to_base(255, 16) == "ff"
    assert from_base("ff", 16) == 255
    assert to_base(0, 10) == "0"
    assert to_base(100, 2) == "1100100"
    assert from_base("1100100", 2) == 100
    # Base58
    data = b"Hello World"
    encoded = base58_encode(data)
    assert base58_decode(encoded) == data
    # Leading zeros
    data2 = b"\x00\x00\x01"
    enc2 = base58_encode(data2)
    assert enc2.startswith("11")
    assert base58_decode(enc2) == data2
    # Base62
    assert from_base(to_base(123456789, 62, B62_ALPHA), 62, B62_ALPHA) == 123456789
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: base_conv.py test")
