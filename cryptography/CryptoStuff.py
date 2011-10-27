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

def column_split(data, length):
    """Split data into elements of given length. The elements are split by
    columns. Example of data with length 5:

    data =  x0  x1  x2  x3  x4
            x5  x6  x7  x8  x9
            x10 x11 x12 x13 x14

            ||  ||  ||  ||  ||

            y0  y1  y2  y3  y4"""
    columns_len = len(data) / length
    for i in range(length):
        round = []
        for j in range(columns_len):
            try:
                round.append(data[i + j*length])
            except IndexError:
                print "broke at i,j"
                break
        yield round
    # last round
    yield round

def vigenere_decrypt(cipher, key, keyspace=26):
    """Decrypt a Vigenere ciphertext with the given key.

    Vigenere is encrypted by:
     e(x1, ..., xm) = (x1 + k1 mod 26, ..., xm + km mod 26)

    where m is the length of the key, and 26 should be the character space.
    Decryption is then:

     d(y1, ..., ym) = (y1 - k1 mod 26, ..., ym - km mod 26)
    """
    ret = []
    for i in range(len(cipher)):
        ret.append(chr(ord(cipher[i]) + ord(key[i%len(key)]) % keyspace))
        # TODO: should append the start of the keyspace, or just return ints and
        # reformat it at output instead - would be easier, i think...
    return ''.join(ret)

def multiplicative_inverse(x, keyspace=26):
    """Find the multiplicative inverse x·¹ so that x * x·¹ == 1, if such a
    variable exists in the given keyspace."""
    # TODO: this is a quite slow process for finding it, trying every possible
    # variable in the keyspace. It will be especially slow if the keyspace is
    # large...
    for i in range(keyspace):
        if (i * x) % keyspace == 1:
            return i

def affine_decrypt(cipher, a, b, modulo=26):
    """Decrypt an affine encrypted ciphertext with the given key."""
    ret = ''
    ainv = multiplicative_inverse(a, modulo)
    for c in cipher:
        cipher = ord(c) - 65
        # TODO: this is not generic, only works for norwegian characters...
        if c == u'Æ': 
            cipher = 26
        elif c == u'Ø':
            cipher = 27
        elif c == u'Å':
            cipher = 28
        plain = (ainv*(cipher - b)) % modulo
        #print "cipher:%s = %s -> %s (%s)" % (c, cipher, plain, chr(plain+65))

        if plain == 26:
            out = u'æ'
        elif plain == 27:
            out = u'ø'
        elif plain == 28:
            out = u'å'
        else:
            out = chr(plain + 97)
        ret += out
    return ret

def equation_solver(matrix, modulo=26):
    """Solve an equation in modulo. The given matrix must be on the form
        ((a, b, y),
         ...
         (a, b, y))
    for equations on the form (xa + b) % modulo = y, e.g. 4a + b % 26 = 11.
    Returns valid results for a and b.
    
    This is usable e.g. for affine cipher solving."""
    ret = []
    for a in range(modulo):
        # get b from first equation
        # TODO: assumes here that matrix[0][1] == 1, should be fixed for other
        # cryptosystems than affine ciphers
        b = (matrix[0][2] - a*matrix[0][0]) % modulo

        correct = False
        for eq in matrix:
            if (a*eq[0] + b*eq[1]) % modulo == eq[2]:
                correct = True
            else:
                correct = False
                break
        if correct:
            ret.append((a,b))
    print ret
    return ret

def lfsr_keystream(startkey, constants):
    """Create a Linear Feedback Shift Register keystream out of a given startkey
    and constants. All is considered binary, but for ease of code, and not much
    time to do this, the input in startkey and constants has to be bytes of 1
    and 0."""
    length = len(startkey)
    assert length == len(constants)
    # first return initial key
    z = list()
    for key in startkey:
        yield key
        z.append(key)
    # then use the constants for following rounds
    i = 0
    while True:
        z.append(0)
        for j in range(len(constants)):
            if not int(constants[j]):
                continue
            z[i+length] += z[i+j]
        z[i+length] = z[i+length] % 2
        yield z[i+length]
        i += 1
    # TODO: could remove old z, as last round is used. Now we quickly use up all
    # the memory.


# The probabilities of characters in some languages
probabilities = {
    'no': {
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
        },
    }

def vigenere_findkey_by_ioc(cipher, keylength, alphabet, target_ioc=0.065):
    """Try to find a proper key by using the index of coincidence over the
    ciphertext.

    The given alphabet must be on the form: {'key': probability, ...}
    """
    key = ''
    partsize = len(cipher) / keylength
    sorted_alph = sorted(alphabet)

    for column in column_split(cipher, keylength):
        count = count_chars(column)
        count = dict((c.lower(), count[c]) for c in count)
        best_key = ('_', 9999)
        for g in range(len(alphabet)):
            idx = 0
            for i in range(len(alphabet)):
                #print "%3d: %s (%s)   %2.3f * %2.3f" % (i, sorted_alph[i], sorted_alph[(i+g)%len(alphabet)],
                #                              alphabet[sorted_alph[i]],
                #                              count.get(sorted_alph[(i+g)%len(alphabet)], 0.0)
                #                              )
                idx += (alphabet[sorted_alph[i]] 
                        * count.get(sorted_alph[(i+g) % len(alphabet)], 0.0))
            if abs(target_ioc - best_key[1]) > abs(target_ioc - idx):
                best_key = (sorted_alph[g], idx)
        print best_key
        key += best_key[0]
    return key


