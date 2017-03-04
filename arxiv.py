#!/usr/bin/env python

import feedparser
import urllib
import wget

import os

if __name__ == "__main__":

    path = "./pdf"

    if not os.path.isdir(path):
        os.mkdir( path, 0755 )

    url = 'http://export.arxiv.org/api/query?search_query=Deep Learning&start=0&max_results=1999'

    data = urllib.urlopen(url).read()
    feed = feedparser.parse(data)

    i = len(feed['entries']) - 1

    while ( i != 0 ):

        try:
            entry = feed['entries'][i]

            title = entry.title
            description =  entry.summary

            j = len(entry.links) - 1

            while ( j != 0 ):
                if(entry.links[j].type == 'application/pdf'):
                    print entry.links[j].href
                    output='./%s/%s.pdf'%(path,title)
                    wget.download(entry.links[j].href, out=output)

                j = j - 1

        except Exception as e:
            print( e )
            print 'corrupted'

        i = i - 1
