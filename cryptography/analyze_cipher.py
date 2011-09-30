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

# Statistical use of Norwegian letters
char_use_no = {
        'a': 6.1,
        'b': 1.5,
        'c': 0.2,
        'd': 4.3,
        'e': 15.2,
        'f': 2.0,
        'g': 3.8,
        'h': 1.6,
        'i': 6.2,
        'j': 1.0,
        'k': 3.8,
        'l': 5.4,
        'm': 3.3,
        'n': 8.1,
        'o': 4.9,
        'p': 1.9,
        'q': 0.004,
        'r': 8.6,
        's': 6.7,
        't': 7.9,
        'u': 1.6,
        'v': 2.5,
        'w': 0.1,
        'x': 0.03,
        'y': 0.7,
        'z': 0.03,
        'æ': 0.2,
        'ø': 0.9,
        'å': 1.5,
        }

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
    counts = count_chars(' '.join(unicode(a, 'utf8') for a in sys.argv[1:]))
    for c in sorted(counts, key=lambda a: counts[a], reverse=True):
        print "%3s : %d" % (c, counts[c])

