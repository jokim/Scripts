#!/usr/bin/env python
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
        u'a': 6.1,
        u'b': 1.5,
        u'c': 0.2,
        u'd': 4.3,
        u'e': 15.2,
        u'f': 2.0,
        u'g': 3.8,
        u'h': 1.6,
        u'i': 6.2,
        u'j': 1.0,
        u'k': 3.8,
        u'l': 5.4,
        u'm': 3.3,
        u'n': 8.1,
        u'o': 4.9,
        u'p': 1.9,
        u'q': 0.004,
        u'r': 8.6,
        u's': 6.7,
        u't': 7.9,
        u'u': 1.6,
        u'v': 2.5,
        u'w': 0.1,
        u'x': 0.03,
        u'y': 0.7,
        u'z': 0.03,
        u'æ': 0.2,
        u'ø': 0.9,
        u'å': 1.5,
        }
# Statistical use of Norwegian bigrams
bigrams_use_no = {
        'er': 2.5,
        'en': 3.2,
        'de': 2.6,
        're': 2.3,
        'te': 1.7,
        'et': 1.7,
        'an': 1.6,
        'in': 1.5,
        'ng': 1.4,
        'es': 1.4,
        'nd': 1.3,
        'ge': 1.3,
        'or': 1.3,
        'st': 1.2,
        'ne': 1.1,
        'ti': 1.1,
        'il': 1.1,
        }


def count_chars(input):
    """Count the number of occurrences of each character and return a dict."""
    counts = {}
    for c in input:
        counts.setdefault(c, 0)
        counts[c] += 1
    return counts

def count_bigrams(input):
    """Count the number of occurrences of all bigrams. Simply counting all
    neighbours."""
    bigrams = {}
    for i in range(len(input)):
        try:
            bigram = input[i] + input[i+1]
        except IndexError:
            return bigrams
        bigrams.setdefault(bigram, 0)
        bigrams[bigram] += 1

def count_grams(input, length=3):
    """Count the number of repetitions of sequences in the ciphertext."""
    grams = {}
    i = 0
    while True:
        try:
            seq = input[i]
            for j in range(1, length):
                seq += input[i + j]
        except IndexError:
            return grams
        grams.setdefault(seq, 0)
        grams[seq] += 1
        i += 1
    return grams

def kasiski(input):
    """Do the kasiski test on a given ciphertext, that is, find repeating
    sequences and get the greated common divisor (gcd) between them. Used for
    finding the key length of different cryptosystems, e.g. Vigenère.
    
    The return is a list of all valid deltas, that is, possible key lengths."""
    deltas = set()

    # Starting high, trying to find larger sequences first
    size = len(input) / 3
    while size >= 3:
        seqs = count_grams(input, length=size)
        for seq in sorted(seqs, key=lambda a: int(seqs[a]), reverse=True):
            # TODO: why doesn't this sort correctly?

            if seqs[seq] <= 2:
                # TODO: ignore those with only two occurences as well?
                continue
            #print seq, seqs[seq]

            # find sequence' positions
            # find gcd of sequence
            poss = []
            pos = -1
            try:
                while True:
                    pos = input.index(seq, pos + 1)
                    poss.append(pos)
            except ValueError:
                pass
            # find gcd between first pos and the rest
            divisor = poss[1] - poss[0]
            for pos in range(2, len(poss)):
                divisor = gcd(divisor, poss[pos] - poss[0])
            deltas.add(divisor)
        size -= 1
    return deltas

def gcd(a,b):
    """Finding the greatest common divisor between two integers"""
    while b: 
        a, b = b, a%b
    return a

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: analyze <input-data to analyze>"
        sys.exit(1)
    if '--norwegian' in sys.argv[1:]:
        print "Statistics for Norwegian:"
        print "Chars"
        for c in sorted(char_use_no, key=lambda a: char_use_no[a], reverse=True):
            print u"%5s : %5.4f" % (c, char_use_no[c])
        print "Bigrams"
        for bi in sorted(bigrams_use_no, key=lambda a: bigrams_use_no[a], reverse=True):
            print u"%5s : %5.4f" % (bi, bigrams_use_no[bi])
        sys.exit()

    cipher = ' '.join(unicode(a, 'utf8') for a in sys.argv[1:])
    counts = count_chars(cipher)
    print "    Char Occur    Percent"
    for c in sorted(counts, key=lambda a: counts[a], reverse=True):
        print "%5s : %5d    %1.4f" % (c, counts[c], float(counts[c])/len(cipher))
    print "Total    %5d" % len(cipher)

    print "\nBigrams:"
    bigrams = count_bigrams(cipher.replace(' ', ''))
    for bi in sorted(bigrams, key=lambda a: bigrams[a], reverse=True):
        if bigrams[bi] <= 1: # drop single ones, they're not interesting
            break
        print "%5s : %5d" % (bi, bigrams[bi])

    print

    print "Kasiski:"
    keylengths = kasiski(cipher.replace(' ', ''))
    print "Possible key lengths: %s" % ', '.join(str(k) for k in keylengths)
