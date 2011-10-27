#!/bin/env python
# -*- encoding: utf8 -*-
"""Small script just for fixing task 3 in oblig, UNIK4220.  """
import CryptoStuff

# Encoding of characters to given code values in oblig.
encoding = {
        u'A': u'00000',
        u'B': u'00001',
        u'C': u'00010',
        u'D': u'00011',
        u'E': u'00100',
        u'F': u'00101',
        u'G': u'00110',
        u'H': u'00111',
        u'I': u'01000',
        u'J': u'01001',
        u'K': u'01010',
        u'L': u'01011',
        u'M': u'01100',
        u'N': u'01101',
        u'O': u'01110',
        u'P': u'01111',
        u'Q': u'10000',
        u'R': u'10001',
        u'S': u'10010',
        u'T': u'10011',
        u'U': u'10100',
        u'V': u'10101',
        u'W': u'10110',
        u'X': u'10111',
        u'Y': u'11000',
        u'Z': u'11001',
        u'Æ': u'11010',
        u'Ø': u'11011',
        u'Å': u'11100',
        u' ': u'11101',
        u'.': u'11110',
        u',': u'11111',
        }
decoding = dict((encoding[k], k) for k in encoding)

keystream = CryptoStuff.lfsr_keystream((0,1,0,1,0,1,0,1),
                                       (1,1,0,0,0,1,1,0))

cipher = u'NQFTRQBNCJK,ØDXDUVZØ,EAQDX'
binary_cipher = ''.join(encoding[s] for s in cipher)
print "Coded input: %s" % binary_cipher

plain_coded = list()
for c in binary_cipher:
    c = int(c)
    z = keystream.next()
    plain_coded.append(z ^ c)
print "Coded output: %s" % ''.join(str(p) for p in plain_coded)

plain = ''
for i in range(len(plain_coded) / 5):
    ret = ''.join(str(p) for p in plain_coded[i*5:i*5+5])
    print "plplpl: %s" % ret
    plain += decoding[ret]
print "Plain: %s" %plain








