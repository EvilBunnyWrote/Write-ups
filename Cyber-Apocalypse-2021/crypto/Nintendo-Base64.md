# Nintendo Base64

## Problem

Aliens are trying to cause great misery for the human race by using our own cryptographic technology to encrypt all our games.
Fortunately, the aliens haven't played CryptoHack so they're making several noob mistakes. Therefore they've given us a chance to recover our games and find their flags.
They've tried to scramble data on an N64 but don't seem to understand that encoding and ASCII art are not valid types of encryption!

[Task file](files/crypto_nintendo_base64.zip)

## Solution

We are given file with ascii-art formatted text, which seems to be base64, let's decode it:

```sh
> cat output.txt | xargs echo -n | sed 's/ //g' | base64 -d
Vm0xNFlWVXhSWGxUV0doWVlrZFNWRmx0ZUdGalZsSlZWR3RPYWxKdGVIcFdiR2h2VkdzeFdGVnViRmRXTTFKeVdWUkdZV1JGT1ZWVmJGWk9WakpvV1ZaclpEUlVNVWw0Vkc1U1RsWnNXbGhWYkZKWFUxWmFSMWRzV2s1V2F6VkpWbTEwYjFkSFNsbFZiRkpXWWtaYU0xcEZXbUZTTVZaeVkwVTFWMDFHYjNkV2EyTXhWakpHVjFScmFGWmlhM0JYV1ZSR1lWZEdVbFZTYms1clVsUldTbGRyV2tkV2JGcEZVVlJWUFE9PQ==
```

And few more times:

```sh
cat output.txt | xargs echo -n | sed 's/ //g' | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d | base64 -d
CHTB{3nc0d1ng_n0t_3qu4l_t0_3ncrypt10n}
```


## TL;DR

 - Base64 encoding formatted to be a bit confusing
