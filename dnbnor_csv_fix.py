#!/bin/env python
# -*- encoding:utf8 -*- #
#
# Copyright 2011, 2012 Joakim Hovlandsvåg <joakim.hovlandsvag@gmail.com>
#
# This file is just a small script of mine.
# 
# This is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HomebaseTweaks. If not, see <http://www.gnu.org/licenses/>.
"""Fixing DNB's CSV files, as they don't have the correct formatting to be read
by GnuCash without errors. It takes the CSV files as arguments, and prints the
washed format to stdout, so you could pipe to a proper file.

Example:

    dnb2csv.py maanedoversikt.april.txt > brukskonto.2012.04.txt

"""
import sys
import os

def usage(exitcode = 0):
    print """Usage: %(file)s <account.csv> [<account2.csv> ...]

    %(doc)s

    -h, --help      Show this and quit.

    Reads the csv files and prints it out to stdout, in a more readable format
    for GnuCash.""" % {'file': os.path.basename(sys.argv[0]),
                       'doc': __doc__}
    sys.exit(exitcode)

def process_line(line):
    """Process a line in csv format and return it in the correct format.
    """
    # gnucash doesn't seem to like too much spaces:
    while line.find('  ') != -1:
        line = line.replace('  ', ' ')
    # remove weird characters:
    line = line.replace('\r', ' ')
    line = line.replace('\t', ' ')
    line = line.replace('\n', ' ')
    line = line.replace('\0', ' ')
    line = line.replace('&amp;', '&')
    line = line.replace('  ', ' ')

    values = line.strip().split(';')

    # the two last contains values, so commas should be replaced with points
    values[-2] = values[-2].replace(',', '.')
    values[-1] = values[-1].replace(',', '.')
    out = u';'.join(values)
    print out.encode('utf-8')

def process_file(filename):
    f = open(filename, 'r')
    line = unicode(f.readline(), 'iso-8859-1')
    if not any(line.startswith(s) for s in ('Dato', '"Dat')):
        # skipping the first line if it's the value names
        process_line(line)
    for line in f:
        if line.strip():
            line = unicode(line, 'iso-8859-1')
            process_line(line)

def main(argv):
    if len(argv) <= 1:
        print "Need to specify what csv file(s) to fix."
        usage(1)
        sys.exit(2)
    if '-h' in argv or '--help' in argv:
        usage()

    for f in argv[1:]:
        process_file(f)

if __name__ == '__main__':
    main(sys.argv)

