#!/bin/env python
# -*- encoding: utf8 -*-
"""Small script just for fixing task 3 in oblig, UNIK4220.  """
import CryptoStuff

print "Oppgave 3b)\n"

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
keys = ''

cipher = u'NQFTRQBNCJK,ØDXDUVZØ,EAQDX'
binary_cipher = ''.join(encoding[s] for s in cipher)
print "Coded input: %s" % binary_cipher

plain_coded = list()
for c in binary_cipher:
    c = int(c)
    z = keystream.next()
    keys += str(z)
    plain_coded.append(z ^ c)
print "Keystream used: %s" % keys
print "Coded output: %s" % ''.join(str(p) for p in plain_coded)

plain = ''
for i in range(len(plain_coded) / 5):
    ret = ''.join(str(p) for p in plain_coded[i*5:i*5+5])
    plain += decoding[ret]
print "Plain: %s" %plain

print "\nOppgave 3c)\n"

cipher = u'RPPSTTOXPVFMAVØD,UÅÅPLYWUQÆLZFÅJVÅS UN.ODH'
binary_cipher = ''.join(encoding[s] for s in cipher)
print "Coded input: %s" % binary_cipher

hei = ''.join(encoding[s] for s in 'HEI,')
print "Hei: %s" % hei
initkey = ''
for i in range(len(hei)):
    initkey += str(int(hei[i]) ^ int(binary_cipher[i]))
print "Initial key: %s" % initkey
    
print "Brute force:"
possibilities = (
        '00000000',
        '00000001',
        '00000010',
        '00000011',
        '00000100',
        '00000101',
        '00000110',
        '00000111',
        '00001000',
        '00001001',
        '00001010',
        '00001011',
        '00001100',
        '00001101',
        '00001110',
        '00001111',
        '00010000',
        '00010001',
        '00010010',
        '00010011',
        '00010100',
        '00010101',
        '00010110',
        '00010111',
        '00011000',
        '00011001',
        '00011010',
        '00011011',
        '00011100',
        '00011101',
        '00011110',
        '00011111',
        '00100000',
        )


key = (1, 0, 1, 1, 0, 0, 1, 0) 
for i in range(len(possibilities)):
    keystream = CryptoStuff.lfsr_keystream(key,
                                possibilities[i])

