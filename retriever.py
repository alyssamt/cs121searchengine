import os
import re
import sys
import json
import time
import string
from collections import defaultdict


class Retriever(object):

    def __init__(self, index_file="index.txt"):
        self.load_index(index_file)


    def load_index(self, index_file):
        # Load index and document map
        print("Loading index... (~8 seconds)")
        with open(index_file, 'r') as f:
            str = f.read()
            self.index = json.loads(str)

        print("Loading document map...")
        with open("WEBPAGES_CLEAN/bookkeeping.json", 'r') as f:
            self.doc_map = json.loads(f.read())


    def retrieve(self, terms):
        #print("SEARCH TERMS: {}".format(terms))
        all_links = []

        # Search for term(s)
        for t in terms:
            cur_links = set()

            if t in self.index.keys():
                for doc in self.index[t]:
                    cur_links.add(self.doc_map[doc])

            all_links.append(cur_links)

        final_links = all_links[0]

        # For multiple terms, find intersection
        if len(terms) > 1:
            for i in range(1, len(all_links)):
                final_links = final_links.intersection(all_links[i])

        return final_links


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("USAGE: python retriever.py <term>")
        exit()

    retrieve(sys.argv[1:])

