# PhaseStream 1

## Problem

The aliens are trying to build a secure cipher to encrypt all our games called "PhaseStream". They've heard that stream ciphers are pretty good. The aliens have learned of the XOR operation which is used to encrypt a plaintext with a key. They believe that XOR using a repeated 5-byte key is enough to build a strong stream cipher. Such silly aliens! Here's a flag they encrypted this way earlier. Can you decrypt it (hint: what's the flag format?) 2e313f2702184c5a0b1e321205550e03261b094d5c171f56011904

## Solution

We are given XOR'ed flag and key length which is exactly the size of known part of the flag: `CHTB{`. XOR'ing those first 5 bytes with leaked part we get they key which we use to decrypt the flag:

```python
import re
from binascii import unhexlify, hexlify

def xorstr(str1, str2):
    return [char1^char2 for char1, char2 in zip(str1, str2)]

ct = unhexlify(b"2e313f2702184c5a0b1e321205550e03261b094d5c171f56011904")
leaked = b"CHTB{"

key = xorstr(ct[:5], leaked) * len(ct)

print("".join([chr(char) for char in xorstr(key, ct)]))
```
```
> python solve.py
CHTB{u51ng_kn0wn_pl41nt3xt}
```

## TL;DR

 - XOR cipher
 - Flag format leaks first 5 bytes
 - Key is 5 bytes
 - XOR again to get the key
