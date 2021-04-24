# PhaseStream 2

## Problem

The aliens have learned of a new concept called "security by obscurity". Fortunately for us they think it is a great idea and not a description of a common mistake. We've intercepted some alien comms and think they are XORing flags with a single-byte key and hiding the result inside 9999 lines of random data, Can you find the flag?

[Task file](files/crypto_ps2.zip)

## Solution

We are given 10000 lines of ciphertexts and key length of 1. Such short key can be easily bruteforced, especially if we know what to look for, which we do (flag format).

A bit more neat approach would be to write bruteforce script ourselves, but CTF is more about speed than quality, so we'll just use [xortool](https://github.com/hellman/xortool):

```sh
# -x to unhex
# -b to bruteforce most frequent chars
# -l 1 to look for 1-byte key
> xortool -x -b -l 1 output.txt
256 possible key(s) of length 1:
\x94
\x95
\x96
\x97
\x90
...
Found 0 plaintexts with 95%+ valid characters
See files filename-key.csv, filename-char_used-perc_valid.csv

> grep -ao "CHTB{.*}" xortool_out/*
xortool_out/209.out:CHTB{n33dl3_1n_4_h4yst4ck}
```

## TL;DR

 - Known key length (short)
 - Known partial plaintext (flag format)
 - Bruteforce it
