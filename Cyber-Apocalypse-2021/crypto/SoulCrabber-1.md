# SoulCrabber 1

## Problem

Aliens heard of this cool newer language called Rust, and hoped the safety it offers could be used to improve their stream cipher.

[Task file](files/crypto_soulcrabber.zip)

## Solution

We are given a ciphertext and a source code: it's a simple XOR cipher. Source code leaks a PRNG seed, which is hardcoded there, so we can just regenerate the sequence, which is used as a key:

```rust
use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;

fn main() -> std::io::Result<()> {
    let mut rng = StdRng::seed_from_u64(13371337);
    for _ in 0..64{
        print!("{},", rng.gen::<u8>());
    }
    Ok(())
}
```

```sh
> cargo run
88,17,64,198,160,251,74,26,178,163,56,85,137,126,94,188,38,83,116,2,190,130,239,11,12,99,232,148,14,107,27,194,98,21,224,135,61,173,116,148,78,124,152,228,207,8,46,78,193,79,116,202,239,198,46,213,233,92,108,151,207,246,177,172,
```

We pass the key to a script to decode it:

```python
import re
from binascii import unhexlify

def xorstr(str1, str2):
    return [char1^char2 for char1, char2 in zip(str1, str2)]

ct = unhexlify(b"1b591484db962f7782d1410afa4a388f7930067bcef6df546a57d9f873")
key = [88,17,64,198,160,251,74,26,178,163,56,85,137,126,94,188,38,83,116,2,190,130,239,11,12,99,232,148,14,107,27,194,98,21,224,135,61,173,116,148,78,124,152,228,207,8,46,78,193,79,116,202,239,198,46,213,233,92,108,151,207,246,177,172]

print("".join([chr(char) for char in xorstr(ct, key)]))
```

```sh
> python solve.py
CHTB{mem0ry_s4f3_crypt0_f41l}
```

## TL;DR

  - XOR cipher
  - Hardcoded PRNG seed
  - Regenerate rand sequence
