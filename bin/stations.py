#!/usr/bin/env python

import csv
import re
import sys

import requests


def station_csv(inpath=None, outpath=None):
    """
    Given a csv of station ids, names, eastings, northings, latitudes and
    longitudes as input, write a csv of station ids, names, postcodes, eastings
    and northings to the given output.
    """
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
        for id, name, x, y, lat, lng in reader:
            postcode = get_postcode(lat, lng)
            writer.writerow([id, name, postcode, x, y])
    finally:
        infile.close()
        outfile.close()


def get_postcode(lat, lng):
    url = 'http://uk-postcodes.com/latlng/{lat},{lng}.json'.format(lat=lat, lng=lng)
    resp = requests.get(url)
    resp.raise_for_status()
    return re.sub(r'\s\s+', ' ', resp.json()['postcode'])


if __name__ == '__main__':
    try:
        inpath = sys.argv[1]
    except IndexError:
        inpath = outpath = None
    else:
        try:
            outpath = sys.argv[2]
        except IndexError:
            outpath = None
    station_csv(inpath, outpath)
