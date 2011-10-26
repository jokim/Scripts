#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright Joakim Hovlandsvåg
# Licenced by GPLv3.
"""
Script for handling affine cipher cryptosystems.
"""
import sys
import CryptoStuff

# TODO: handle input better, if more functionality is needed
if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print "Usage: affine.py a b <input-data to analyze>"
        sys.exit(1)
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    for i in range(3, len(sys.argv)):
        #print "%d = %s" % (i, sys.argv[i])
        print CryptoStuff.affine_decrypt(unicode(sys.argv[i], 'utf-8'), a, b, 29),
