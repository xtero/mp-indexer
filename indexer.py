#!/usr/bin/env python
import json
import hashlib
from zipfile import ZipFile
from os import walk
from pprint import pprint

ARCHIVE_REPO="../archiver/archives"

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
with open("index.json", "w") as output:
    json.dump(  data, output )
