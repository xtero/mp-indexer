#!/usr/bin/env python
import json
import hashlib
from zipfile import ZipFile
from os import walk
from pprint import pprint
import argparse
import sys

OUTPUT=sys.stdout

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help="Folder where the indexer will parser zip file", required=True)
parser.add_argument('-o', '--output', help="Output of the script, by default, it will be stdout", default="")

args = parser.parse_args()
if args.output != "":
    try: 
        OUTPUT = open( args.output, "w" )
    except (IOError) as e :
        print("Error on opening file ")

ARCHIVE_REPO = args.input

data = []

def md5sum( path ):
    with open(path, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

for (dirpath, dirnames, filenames) in walk( ARCHIVE_REPO ):
    for filename in filenames:
        path = dirpath + '/' + filename
        with ZipFile( path, 'r' ) as zipf:
            definition = json.load( zipf.open('definition.json') )
            meta = definition['meta']
            meta['md5sum'] = md5sum( path )
            data.append( meta )

json.dump(  data, OUTPUT )
