#!/usr/bin/env python

"""Import data to Open Annotation store over RESTful interface."""

import sys
import urllib2
import codecs
import json

from os import path

import requests

DEFAULT_URL='http://127.0.0.1:5000/annotations/'
DEFAULT_ENCODING='utf-8'

def argparser():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('source', metavar='FILE/DIR', nargs='+',
                        help='Source data to import')
    parser.add_argument('-u', '--url', default=DEFAULT_URL,
                        help='URL for store (default %s)' % DEFAULT_URL)
    return parser

def pretty(doc):
    """Pretty-print JSON."""
    return json.dumps(doc, sort_keys=True, indent=2, separators=(',', ': '))

def read_dir(source):
    raise NotImplementedError

def read_file(source):
    with codecs.open(source, encoding=DEFAULT_ENCODING) as f:
        text = f.read()
    return json.loads(text)

def read_source(source):
    if path.isdir(source):
        return read_dir(source)
    else:
        return read_file(source)

def import_from(source, options):
    """Import data from file or directory source."""

    headers = {'Content-type': 'application/json'}

    data = read_source(source)
    for doc in data['@graph']:
        req = requests.post(options.url, data=json.dumps(doc), headers=headers)

def main(argv):
    args = argparser().parse_args(argv[1:])

    for s in args.source:
        import_from(s, args)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
