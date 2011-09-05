#!/usr/bin/env python
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
This is a small script for calculating the repayment of a given loan at each
term. This was created just to learn how to do it, and get a feeling of the
numbers, as I have no clue about finances.
"""
import sys, getopt

def usage(exitcode=0):
    print "Usage: %s <loan> <rate per year> <# of years> <# of terms per year>" % sys.argv[0]
    print """

    Example:

    A 5% loan at 500 000,- split in 12 terms for 30 years

        nedbetaling.py 500000 0.05 30 12
    """
    sys.exit(exitcode)

def calculate_repayment(loan, rate, years, termsperyear):
    termrate = rate / termsperyear;
    terms = years * termsperyear;
    return loan * ((1 + termrate)**terms * termrate) / ((1 + termrate)**terms - 1)

def main(argv):
    if len(argv) != 5:
        usage(1)
    loan            = float(argv[1])
    rate            = float(argv[2])
    years           = int(argv[3])
    termsperyear    = float(argv[4])

    repayment = calculate_repayment(loan, rate, years, termsperyear)
    print "%.2f" % repayment

if __name__ == '__main__':
    main(sys.argv)
