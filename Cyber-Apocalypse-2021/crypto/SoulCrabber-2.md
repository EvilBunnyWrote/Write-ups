# SoulCrabber 2

## Problem

Aliens realised that hard-coded values are bad, so added a little bit of entropy.

[Task file](files/crypto_soulcrabber_2.zip)

## Solution

We are given a ciphertext and a source code: it's a simple XOR cipher. It seeds PRNG with system time, which we don't know, do we? Let's look closer at the task files:

```sh
> stat out.txt
File: out.txt
Size: 83              Blocks: 8          IO Block: 4096   regular file
Device: 10302h/66306d   Inode: 3945538     Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/  pirate)   Gid: ( 1000/  pirate)
Access: 2021-04-16 14:32:16.000000000 +0300
Modify: 2021-04-16 14:32:16.000000000 +0300
Change: 2021-04-24 16:20:25.543082696 +0300
Birth: 2021-04-24 16:20:25.543082696 +0300
```

Well, seems like we do have original atime and mtime properites, converted to a timestamp: `1618572736`. Let's regenerate rand sequence and decrypt the flag:

```rust
use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;

fn main() -> std::io::Result<()> {
    let mut rng = StdRng::seed_from_u64(1618572736);
    for _ in 0..64 {
        print!("{},", rng.gen::<u8>());
    }
    Ok(())
}
```

```sh
> cargo run
166,34,188,15,53,23,72,60,232,112,179,105,157,244,193,141,24,82,167,23,195,105,203,144,106,72,142,107,174,175,76,100,158,251,77,136,100,231,222,42,83,123,131,251,82,210,102,127,117,56,228,32,29,205,240,95,62,223,163,163,117,64,157,156,
```

Passing it to a decryption script:

```python
import re
from binascii import unhexlify

def xorstr(str1, str2):
    return [char1^char2 for char1, char2 in zip(str1, str2)]

ct = unhexlify(b"418a5175c38caf8c1cafa92cde06539d512871605d06b2d01bbc1696f4ff487e9d46ba0b5aaf659807")
key = [166,34,188,15,53,23,72,60,232,112,179,105,157,244,193,141,24,82,167,23,195,105,203,144,106,72,142,107,174,175,76,100,158,251,77,136,100,231,222,42,83,123,131,251,82,210,102,127,117,56,228,32,29,205,240,95,62,223,163,163,117,64,157,156]

print("".join([chr(char) for char in xorstr(ct, key)]))
```

```sh
> python solve.py
ç¨ízö°ôß▒ECòIzÖwoy@qôýZP▒½÷>H»²T
```

A-a-a-and it's gibberish. Well, let's assume that mtime and atime were intentionally messed up, but left somewhere in the ballpark, in the past. Luckily we know partial plaintext - flag format, so we can bruteforce the the seed until first 5 bytes of random sequence match with the partial key we know.

First, find first 5 bytes of the key:

```python
from binascii import unhexlify

ct = unhexlify(b"418a5175c38caf8c1cafa92cde06539d512871605d06b2d01bbc1696f4ff487e9d46ba0b5aaf659807")

print([a^b for a,b in zip(ct, b"CHTB{")])
```

```sh
> python solve.py
[2, 194, 5, 55, 184]
```

Second, pass it to the bruteforce utility:

```rust
use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;

fn main() -> std::io::Result<()> {
    let initial_timestamp = 1618572736;
    let partial_key: [u8; 5] = [2, 194, 5, 55, 184];
    for current_value in (initial_timestamp-1000000..initial_timestamp).rev() {
        let mut rng = StdRng::seed_from_u64(current_value);
        let first5_sequence: [u8; 5] = [rng.gen::<u8>(), rng.gen::<u8>(), rng.gen::<u8>(), rng.gen::<u8>(), rng.gen::<u8>()];

        if first5_sequence == partial_key {
            println!("Found possible seed: {}", current_value);
            rng = StdRng::seed_from_u64(current_value);
            for _ in 0..64 {
                print!("{},", rng.gen::<u8>());
            }
            break;
        }
    }
    Ok(())
}
```

```sh
> cargo run
Found possible seed: 1618179277
2,194,5,55,184,239,195,184,41,154,152,79,129,101,59,169,61,68,66,14,58,53,237,162,40,203,100,167,128,139,123,16,194,119,212,84,40,218,80,236,122,232,34,12,231,51,129,215,191,228,95,251,123,178,118,82,26,229,162,106,198,0,231,137,
```

Let's try to decrypt with this one:

```python
> python solve.py
CHTB{cl4551c_ch4ll3ng3_r3wr1tt3n_1n_ru5t}
```

It was `Sun Apr 11 2021 22:14:37 GMT+0000` after all, for some reason.

## TL;DR

- XOR cipher
- Approximate PRNG seed leaked in mtime/atime
- Bruteforce seed to regenerate rand sequence
