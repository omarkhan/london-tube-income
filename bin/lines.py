#!/usr/bin/env python

import csv
import json
import sys


def final_json(lines_path, inpath=None, outpath=None):
    """
    Given the path to a json of tube line data, and a csv of station ids,
    names, and incomes as input, write a json listing income data on each path
    through each tube line.
    """
    with open(lines_path, 'rb') as lines_file:
        lines = json.load(lines_file)['lines']
    for line in lines:
        for vert, edges in line['graph'].iteritems():
            line['graph'][vert] = set(edges)

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
        stations = {row[0]: {'name': row[1], 'income': row[2]} for row in reader}
        data = []
        for line in lines:
            branches = []
            for path in line['paths']:
                ln = [stations[s] for s in build_line(line['graph'], path['path'])]
                branches.append({'name': path['name'], 'stations': ln})
            data.append({'name': line['name'], 'id': line['id'], 'branches': branches})
        json.dump({'lines': data}, outfile, indent=2)
    finally:
        infile.close()
        outfile.close()


def follow(graph, start):
    """
    Return a generator for a depth-first search on the line represented by the
    given graph, starting at the given station.

    The graph should be a dict mapping each station to the set of all stations
    it connects to.
    """
    ends = graph.get(start, set())
    yield (start, ends)
    if graph:
        subgraph = {key: value - {start} for key, value in graph.iteritems()
                    if key != start and any(v != start for v in value)}
        for end in ends:
            for vert, edges in follow(subgraph, end):
                yield (vert, edges)


def build_line(graph, path):
    """
    For a given graph, returns the shortest list of stations containing the
    stations in the given path, in the order they are given.
    """
    # Store each station in the line here as we traverse the graph
    line = []

    # Store the index in `line` of each fork in the graph. Once we reach the
    # end of the line, if we don't have the path we want we pop the index and
    # rewind `line` back to that point before continuing.
    forks = []

    start, rest = path[0], path[1:]
    for node, edges in follow(graph, start):
        line.append(node)
        if len(edges) > 1:
            for i in xrange(len(edges) - 1):
                forks.append(len(line))
        elif len(edges) == 0:
            if not rest or list_is_subset(rest, line):
                return line
            fork = forks.pop()
            del line[fork:]


def list_is_subset(a, b):
    """
    Return True if the iterable a is a subset of the iterable b, taking
    ordering into account.
    """
    iter_a = iter(a)
    item = next(iter_a)
    try:
        for x in b:
            if x == item:
                item = next(iter_a)
    except StopIteration:
        return True
    return False


def get_line_ends(graph):
    return {vert for vert, edges in graph.iteritems() if len(edges) == 1}


if __name__ == '__main__':
    lines_path = sys.argv[1]
    try:
        inpath = sys.argv[2]
    except IndexError:
        inpath = outpath = None
    else:
        try:
            outpath = sys.argv[3]
        except IndexError:
            outpath = None
    final_json(lines_path, inpath, outpath)
