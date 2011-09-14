#!/bin/env python
# -*- encoding:utf8 -*- #
#
# Copyright 2011 Joakim Hovlandsvåg <joakim.hovlandsvag@gmail.com>
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
"""
Fixing DnbNOR's csv files, as they doesnt have the correct formatting to be read
by GnuCash.
"""
import sys

def usage(exitcode = 0):
    print """Usage: %s <account.csv> [<account2.csv> ...]

    Reads the csv files and prints it out to stdout, in a more readable format
    for GnuCash."""
    sys.exit(exitcode)

def process_file(filename):



def main(argv):
    if len(argv) <= 1:
        print "Need to specify what csv file(s) to fix."
        sys.exit(2)
    if '-h' in argv or '--help' in argv:
        usage()

    for f in argv[1:]:
        process_file(f)

if __name__ == '__main__':
    main(sys.argv)

