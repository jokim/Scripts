#!/usr/bin/env python
# -*- encoding: utf8 -*-
# Copyright Joakim Hovlandsvåg
# Licenced by GPLv3.
"""
Script for doing substitutions on input.

Should make it quicker to check out ciphertext.
"""
import sys, getopt

def do_longs(opts, opt, longopts, args):
    """This is supposed to change getopt's default behaviour, as we want to use
    any character as a valid opt. For example '--A=b' should substitute all A's
    in ciphertext into a plaintext b."""
    try:
        i = opt.index('=')
    except ValueError:
        optarg = None
    else:
        opt, optarg = opt[:i], opt[i+1:]

    try:
        has_arg, opt = getopt.long_has_args(opt, longopts)
    except getopt.GetoptError:
        # opt isn't defined, but we want to use it anyway
        # an argument is always required
        has_arg = True 
    if has_arg:
        if optarg is None:
            if not args:
                raise getopt.GetoptError('option --%s requires argument' % opt, opt)
            optarg, args = args[0], args[1:]
    elif optarg is not None:
        raise getopt.GetoptError('option --%s must not have an argument' % opt, opt)
    opts.append(('--' + opt, optarg or ''))
    return opts, args

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: substitute.py [--a=e --b=f] <input to make substitutions>"
        sys.exit(1)

    # overwrite getopt to our needs
    getopt.do_longs = do_longs

    subs = {}

    opts, args = getopt.getopt(sys.argv[1:], '')

    for opt, arg in opts:
        if opt.startswith('--'):
            subs[opt[2:]] = arg

    if not subs:
        print "No substitutions given... plaintex = ciphertext"
        sys.exit(1)

    cipher = ' '.join(args)

    has_allmatch = cipher.find('*') != -1

    for sub in subs:
        cipher = cipher.replace(sub, subs[sub])
    # Special match for setting unchanged ciphers to a default value
    # We have to assume that the substituted keys aren't present in the
    # ciphertext, to make things simple for now
    if subs.has_key('*') and not has_allmatch:
        changed = subs.values()
        for i in range(len(cipher)):
            if cipher[i] not in changed:
                print "not in"
                cipher = cipher.replace(cipher[i], subs['*'])
    print cipher

