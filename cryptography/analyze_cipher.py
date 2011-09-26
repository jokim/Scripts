#!/bin/env python
# -*- encoding: utf8 -*-
# Copyright Joakim Hovlandsvåg
# Licenced by GPLv3.
"""
A simple script for doing a basic analysis of a given ciphertext. It counts up
the number of occurrences of each character, which is usable if the encryption
is done with plain substitutions.
"""

import sys

def count_chars(input):
    """Count the number of occurrences of each character and return a dict."""
    counts = {}
    for c in input:
        counts.setdefault(c, 0)
        counts[c] += 1
    return counts

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: analyze <input-data to analyze>"
        sys.exit(1)
    counts = count_chars(' '.join(sys.argv[1:]))
    for c in sorted(counts):
        print "%3s : %d" % (c, counts[c])

