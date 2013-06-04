#!/usr/bin/env python

import csv
import sys


def incomes_csv(incomes_path, inpath=None, outpath=None):
    """
    Given the path to the csv of neighbourhood statistics household income
    data, and a csv of station ids, names, and MSOA names as input, write a csv
    of station ids, names and weekly household income estimates.
    """
    # Build a map of MSOA names to weekly household incomes
    with open(incomes_path) as incomes_file:
        # Skip the first 6 lines
        for i in xrange(6):
            next(incomes_file)
        reader = csv.reader(incomes_file)
        incomes = {row[9]: row[12] for row in reader}

    if inpath:
        infile = open(inpath, 'rb')
    else:
        infile = sys.stdin
    if outpath:
        outfile = open(outpath, 'wb')
    else:
        outfile = sys.stdout

    try:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for id, name, area in reader:
            writer.writerow([id, name, incomes[area]])
    finally:
        infile.close()
        outfile.close()


if __name__ == '__main__':
    incomes_path = sys.argv[1]
    try:
        inpath = sys.argv[2]
    except IndexError:
        inpath = outpath = None
    else:
        try:
            outpath = sys.argv[3]
        except IndexError:
            outpath = None
    incomes_csv(incomes_path, inpath, outpath)
