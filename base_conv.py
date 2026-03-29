#!/usr/bin/env python3
"""Base Converter - Convert numbers between any bases (2-64)."""
import sys

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

def to_base(n, base):
    if n == 0: return "0"
    neg = n < 0; n = abs(n); result = []
    while n: result.append(DIGITS[n % base]); n //= base
    return ("-" if neg else "") + "".join(reversed(result))

def from_base(s, base):
    neg = s.startswith("-"); s = s.lstrip("-"); n = 0
    for c in s: n = n * base + DIGITS.index(c)
    return -n if neg else n

def main():
    if len(sys.argv) < 2:
        n = 255
    else:
        n = sys.argv[1]
        if len(sys.argv) > 2:
            src_base = int(sys.argv[2])
            n = from_base(n, src_base)
        else:
            n = int(n, 0)
    print(f"=== Base Converter ===\nDecimal: {n}\n")
    for base, name in [(2,"Binary"),(8,"Octal"),(10,"Decimal"),(16,"Hex"),(32,"Base32"),(36,"Base36"),(64,"Base64")]:
        print(f"  {name:8s} (base {base:2d}): {to_base(n, base)}")
    if len(sys.argv) > 3:
        dst = int(sys.argv[3])
        print(f"\n  Target base {dst}: {to_base(n, dst)}")

if __name__ == "__main__":
    main()
