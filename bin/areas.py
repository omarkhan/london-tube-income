#!/usr/bin/env python

import csv
import math
import re
import sys

import lxml.etree
import requests


HIERARCHY = '2'
LONDON = '276706'


def areas_csv(inpath=None, outpath=None):
    """
    Given a csv with station ids, names, postcodes, eastings and northings,
    write a csv of station ids, names, and ONS mid-layer super output area
    names.
    """
    get_name = get_msoa_name()

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
        for id, name, postcode, x, y in reader:
            area = get_name(postcode, int(x), int(y))
            writer.writerow([id, name, area])
    finally:
        infile.close()
        outfile.close()


def get_msoa_name():
    """
    Return a function that takes a postcode, easting and northing and returns
    the matching MSOA name.
    """
    url = 'http://neighbourhood.statistics.gov.uk/NDE2/Disco/'

    def get_children(area_id):
        resp = requests.get(url + 'GetAreaChildren', params={
            'AreaId': area_id
        })
        resp.raise_for_status()
        tree = lxml.etree.fromstring(resp.content)
        for child in tree.iterfind('.//{*}Area'):
            child_id = child.find('{*}AreaId').text.strip()
            child_name = child.find('{*}Name').text.strip()
            sys.stderr.write('Fetching details for %s\n' % child_name)
            resp = requests.get(url + 'GetAreaDetail', params={
                'AreaId': child_id
            })
            resp.raise_for_status()
            tree = lxml.etree.fromstring(resp.content)
            envelope = tree.find('.//{*}AreaDetail/{*}Envelope').text.strip()
            x1, y1, x2, y2 = map(int, envelope.split(':'))
            midx = x1 + ((x2 - x1) / 2)
            midy = y1 + ((y2 - y1) / 2)
            yield (child_id, child_name, midx, midy)

    def get_closest(x, y, points):
        closest = None
        selected = None
        for idx, (xi, yi) in enumerate(points):
            distance = math.sqrt(((x - xi) ** 2) + ((y - yi) ** 2))
            if closest is None or distance < closest:
                closest = distance
                selected = idx
        return selected

    boroughs = tuple((borough, tuple(get_children(borough[0])))
                      for borough in get_children(LONDON))

    def inner(postcode, x, y):
        """
        Calls the neighbourhood statistics api to fetch the 2001 MSOA for the
        given postcode. If that fails (the api doesn't seem to have a full
        dataset for 2001 MSOAs), try to work out which MSOA we want based on
        the given easting and northing.
        """
        resp = requests.get(url + 'FindAreas', params={
            'HierarchyId': HIERARCHY,
            'Postcode': re.sub(r'\s+', '', postcode)
        })
        resp.raise_for_status()
        tree = lxml.etree.fromstring(resp.content)
        borough = None
        for area in tree.iterfind('.//{*}Area'):
            hierarchy = area.find('{*}HierarchyId').text.strip()
            level = area.find('{*}LevelTypeId').text.strip()
            if hierarchy == HIERARCHY and level == '140':
                return area.find('{*}Name').text.strip()

        sys.stderr.write('Could not find MSOA with postcode %s, trying all '
                         'areas in borough\n' % postcode)
        borough, areas = boroughs[get_closest(x, y, (b[0][2:4] for b in boroughs))]
        return areas[get_closest(x, y, (a[2:4] for a in areas))][1]

    return inner


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
    areas_csv(inpath, outpath)
