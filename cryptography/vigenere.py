#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright Joakim Hovlandsvåg
# Licenced by GPLv3.
"""
A script for decrypting Vigenère-encrypted ciphertexts.
"""
import sys, getopt

import CryptoStuff

def usage(exitcode=0):
    print """Usage: vigenere.py [--key KEY] <ciphertext>

    If no key is given, the ciphertext is analyzed.
    """
    sys.exit(exitcode)

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                '', ['key=', 'keylength='])
    except getopt.GetoptError, e:
        print e
        usage(1)

    if not args:
        print "Need ciphertext as input"
        usage(1)

    key = chosen_keylength = None
    
    for opt, arg in opts:
        if opt == '--key':
            key = arg
        elif opt == '--keylength':
            chosen_keylength = int(arg)


    cipher = ''.join(unicode(a, 'utf8') for a in args)

    if key:
        print CryptoStuff.vigenere_decrypt(cipher, key)
    else:
        print "Possible key lengths (kasiski):"
        print "(The English language's coincidence index is around 0.065)"
        best_length = 0
        goal = 0.065
        for keylength in CryptoStuff.kasiski(cipher):
            idx = [CryptoStuff.index_of_coincidence(chunk) for chunk 
                                                  in CryptoStuff.chunk_split(cipher, keylength)]
            median = sorted(idx)[len(idx) / 2]
            if abs(goal - best_length) > abs(goal - median):
                best_length = keylength
            print "Length %6d : %.4f" % (keylength, median)

        if not chosen_keylength:
            keylength = best_length
            print "\nBest found keylength: %d" % best_length
        else:
            keylength = chosen_keylength 
            print "\nKeylength chosen to: %d" % chosen_keylength

        # TODO: find best values for the chars in the key


