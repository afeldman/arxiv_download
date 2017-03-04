#!/usr/bin/env python

import feedparser
import urllib
import wget
import argparse
import os
import sys

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-q","--query", help="query string")
    parser.add_argument("-m","--max_results", help="Maximal number of results", type=int, default = 10)
    parser.add_argument("-d","--download", help="no Download of the PDF", action="store_true")
    args = parser.parse_args()

    path = "./pdf"

    if not os.path.isdir(path):
        os.mkdir( path, 0755 )

    max_results = args.max_results

    if max_results > 1999:
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

#            description =  entry.summary

            j = len(entry.links) - 1

            while ( j != 0 ):
                if(entry.links[j].type == 'application/pdf' and not args.download):
                    output='./%s/%s.pdf'%(path,title)
                    wget.download(entry.links[j].href, out=output)

                j = j - 1

        except Exception as e:
            print( e )
            print 'corrupted'
            sys.exit(1)

        i = i - 1
