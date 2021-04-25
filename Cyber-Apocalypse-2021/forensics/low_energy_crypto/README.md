##Discovery
[task file](files/forensics_low_energy_crypto.zip)

Unpack file and open pcap in wireshark

Check packets for any received / transmitted data to find anything interesting

At first we found two parts of public key
![First part of key](files/pub_key1.png)
![Second part of key](files/pub_key2.png)

And then as a reply we got somethting that may be a cyphertext
![Ciphertext key](files/ciphertext.png)
Lets export it to file le_flag.bin
![Export ciphertext](files/export_ciphertext.png)

So we have public key and it looks quite short, possibly we can recover private key from it and decode our ciphertext
let use RsaCtfTool for that
```command
RsaCtfTool/RsaCtfTool.py --publickey pub.key --uncipherfile ./le_flag.bin --verbose --private
```

```output
[*] Performing hastads attack.
[*] Performing prime_n attack.
[*] Performing factordb attack.
-----BEGIN RSA PRIVATE KEY-----
MIIBRwIBAAJBAKKPHxnmkWVC4fje7KMbWZf07zR10D0mB9fjj4tlGkPOW+f8JGzg
YJRWboekcnZfiQrLRhA3REn1lUKkRAnUqAkCEQDL/3Li4l+RI2g0FqJvf3ffAkBY
f1ugn3b6H1bdtLy+J6LCgPH+K1E0clPrprjPjFO1pPUkxafxs8OysMDdT5VBx7dZ
RSLx7cCfTVWRTKSjwYKPAiEAy/9y4uJfkSNoNBaib393y3GZu+QkufE43A3BMLPC
ED8CIQDL/3Li4l+RI2g0FqJvf3fLcZm75CS58TjcDcEws8I1twIgJXpkF+inPgZE
TjVKdec6UGg75ZwW3WTPEoVANux3DscCIDjx+RSYECVaraeGG2O/v8iKe6dn1GpM
VGUuaKecISArAiA0QRYkZFB5D4BnOxGkMX3ihjn7NFPQ7+Jk/abWRRq6+w==
-----END RSA PRIVATE KEY-----
Traceback (most recent call last):
  File "RsaCtfTool/RsaCtfTool.py", line 106, in decrypt
    stderr=DN)
  File "/usr/lib/python3.5/subprocess.py", line 316, in check_output
    **kwargs).stdout
  File "/usr/lib/python3.5/subprocess.py", line 398, in run
    output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['openssl', 'rsautl', '-raw', '-decrypt', '-in', '/tmp/tmpogacy33z', '-inkey', '/tmp/tmpxuvyjqnd']' returned non-zero exit status 1

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "RsaCtfTool/RsaCtfTool.py", line 810, in <module>
    attackobj.attack()
  File "RsaCtfTool/RsaCtfTool.py", line 620, in attack
    self.unciphered = self.priv_key.decrypt(self.cipher)
  File "RsaCtfTool/RsaCtfTool.py", line 109, in decrypt
    return self.key.decrypt(cipher)
  File "/usr/lib/python3/dist-packages/Crypto/PublicKey/RSA.py", line 174, in decrypt
    return pubkey.pubkey.decrypt(self, ciphertext)
  File "/usr/lib/python3/dist-packages/Crypto/PublicKey/pubkey.py", line 93, in decrypt
    plaintext=self._decrypt(ciphertext)
  File "/usr/lib/python3/dist-packages/Crypto/PublicKey/RSA.py", line 237, in _decrypt
    cp = self.key._blind(ciphertext, r)
ValueError: Message too large
```
it seems that something go wrong but we recovered private key, let save key to priv.key file and get more info about it

```command
openssl rsa -text -noout -in priv.key
```

```private key info
Private-Key: (512 bit)
modulus:
00:a2:8f:1f:19:e6:91:65:42:e1:f8:de:ec:a3:1b:
59:97:f4:ef:34:75:d0:3d:26:07:d7:e3:8f:8b:65:
1a:43:ce:5b:e7:fc:24:6c:e0:60:94:56:6e:87:a4:
72:76:5f:89:0a:cb:46:10:37:44:49:f5:95:42:a4:
44:09:d4:a8:09
publicExponent:
00:cb:ff:72:e2:e2:5f:91:23:68:34:16:a2:6f:7f:
77:df
privateExponent:
58:7f:5b:a0:9f:76:fa:1f:56:dd:b4:bc:be:27:a2:
c2:80:f1:fe:2b:51:34:72:53:eb:a6:b8:cf:8c:53:
b5:a4:f5:24:c5:a7:f1:b3:c3:b2:b0:c0:dd:4f:95:
41:c7:b7:59:45:22:f1:ed:c0:9f:4d:55:91:4c:a4:
a3:c1:82:8f
prime1:
00:cb:ff:72:e2:e2:5f:91:23:68:34:16:a2:6f:7f:
77:cb:71:99:bb:e4:24:b9:f1:38:dc:0d:c1:30:b3:
c2:10:3f
prime2:
00:cb:ff:72:e2:e2:5f:91:23:68:34:16:a2:6f:7f:
77:cb:71:99:bb:e4:24:b9:f1:38:dc:0d:c1:30:b3:
c2:35:b7
exponent1:
25:7a:64:17:e8:a7:3e:06:44:4e:35:4a:75:e7:3a:
50:68:3b:e5:9c:16:dd:64:cf:12:85:40:36:ec:77:
0e:c7
exponent2:
38:f1:f9:14:98:10:25:5a:ad:a7:86:1b:63:bf:bf:
c8:8a:7b:a7:67:d4:6a:4c:54:65:2e:68:a7:9c:21:
20:2b
coefficient:
34:41:16:24:64:50:79:0f:80:67:3b:11:a4:31:7d:
e2:86:39:fb:34:53:d0:ef:e2:64:fd:a6:d6:45:1a:
ba:fb
```

private key is 512bit therefore ciphertext length has to be multiple 512bit
let examine ciphertext file in hex editor
![examine ciphertext](files/ciphertext_hex.png)
we can see that starting from 0x40 offset file is filled by zero bytes, 0x40 is multiple to 512 bit so let remove zero bytes from the end of file and try to decrypt encoded message

```decrypt command
openssl rsautl -decrypt -inkey priv.key -in le_flag.b -out key.bin
```
and we see no errors, let check decoded message

```check decoded message
cat key.bin
CHTB{5p34k_fr13nd_4nd_3n73r}
```