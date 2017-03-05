#!/usr/bin/env python

import feedparser
import urllib
import wget
import argparse
import os
import hashlib

file_dict = {}

def hash_bytestr_iter(bytesiter, hasher, ashexstr=False):
    for block in bytesiter:
        hasher.update(block)
    return (hasher.hexdigest() if ashexstr else hasher.digest())

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

if __name__ == "__main__":

#argument settings

    parser = argparse.ArgumentParser()
    parser.add_argument("-q","--query", help="query string")
    parser.add_argument("-m","--max_results", help="Maximal number of results", type=int, default = 10)
    parser.add_argument("-d","--download", help="no Download of the PDF", action="store_true")
    parser.add_argument("-p","--prefix", help="download dir", default="./pdf")
    args = parser.parse_args()

# set prefix and build directionary for dublicates
    path = os.path.join(args.prefix, args.query)
    fnamelst = []

    if not os.path.exists(path):
        os.makedirs( path, 0755 )
    else:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".pdf"):
                    fnamelst.append(os.path.join(root, file))

        for fname in fnamelst:
            pos = hash_bytestr_iter(file_as_blockiter(open(fname, 'rb')), hashlib.sha256())
            if file_dict.has_key(pos):
                print 'delete %s'%fname
                os.remove(fname)
            else:
                file_dict[pos]=fname

    #check the maximal number of results

    max_results = args.max_results

    if max_results >= 2000:
        max_results = 1999

    url = 'http://export.arxiv.org/api/query?search_query=%s&start=0&max_results=%s'%(args.query,max_results)

    data = urllib.urlopen(url).read()
    feed = feedparser.parse(data)

    i = len(feed['entries']) - 1

    while ( i != 0 ):

        try:
            entry = feed['entries'][i]

            title = entry.title
            print title

            j = len(entry.links) - 1

            while ( j != 0 ):
                if(entry.links[j].type == 'application/pdf' and not args.download):
                    output='%s/%s.pdf'%(path,title)
                    wget.download(entry.links[j].href, out=output)

                    out_file = hash_bytestr_iter(file_as_blockiter(open(output, 'rb')), hashlib.sha256())
                    if file_dict.has_key(out_file):
                        print 'delete %s' %out_file
                        os.remove(out_file)
                    else:
                        file_dict[out_file]=output

                j = j - 1

        except Exception as e:
            print( e )
            print 'corrupted'

        i = i - 1

    del file_dict
