#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright Joakim Hovlandsvåg
# Licenced by GPLv3.
"""A collection of different crypto stuff I had need for doing the crypto
analysis'. Just basic, but useful stuff for doing simple cryptosystems."""

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

def index_of_coincidence(input):
    """Calculate the index of coincidence out of a string, which is the
    probability that two random elements in the string are identical.

    English language (characters only) has an index of about 0.065, while a
    completely random string has an index of 0.038. This can be used to figure
    out if some ciphertext is getting closer to plaintext, e.g. when splitting
    up Vigenère cipher into different keylengths."""
    index = 0
    if len(input) <= 1: # TODO: what is correct to return when not enough data?
        return -1
    for (char, counts) in count_chars(input).iteritems():
        n = float(len(input))
        index += counts * (counts - 1) / (n*(n-1))
    return index

def gcd(a,b):
    """Finding the greatest common divisor between two integers"""
    while b: 
        a, b = b, a%b
    return a

def chunk_split(data, size):
    """Split some array like object into chunks of the given size. The last
    chunk might be smaller than the size if len(data) % size != 0."""
    # TODO: aren't there a smarter way of doing this? There's probably some
    # functionality for it in python, just have to find it.
    ret = []
    rounds = len(data) / size
    if len(data) % size:
        rounds += 1
    for i in range(rounds):
        chunk = data[i*size:i*size+size]
        ret.append(chunk)
    return ret


def vigenere_decrypt(cipher, key):
    """Decrypt a Vigenere ciphertext with the given key."""
    for chunk in chunk_split(cipher, len(key)):
        # TODO!
        return "NotImplementedYet"
