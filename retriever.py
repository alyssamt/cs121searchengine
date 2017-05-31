import os
import sys
import json
from collections import defaultdict


def retrieve(terms, index_file="index.txt"):

    # Load index and document map

    print("Loading index")
    with open(index_file, 'r') as f:
        print("Reading {}".format(index_file))
        str = f.read()
        print("Converting to JSON")
        index = json.loads(str)

    print("Loading document map")
    with open("WEBPAGES_CLEAN/bookkeeping.json", 'r') as f:
        doc_map = json.loads(f.read())


    # Search for term(s)

    dirname = "retrieved_links"
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    for t in terms:

        doc_count = 0
        t = t.lower()
        print("Searching for {}".format(t))

        if t not in index:
            print("{} not found in index".format(t))

        fname = "{}/{}.txt".format(dirname, t)

        with open(fname, 'w') as f:
            for doc in index[t]:
                f.write("{}\n".format(doc_map[doc]))
                doc_count += 1

        print("{} links written to {}".format(doc_count, fname))


    # For multiple terms, find intersection

    if len(terms) > 1:

        links = set()
        doc_count = 0
        fname = "{}/{}.txt".format(dirname, '_'.join(terms))

        for t in terms:

            with open("{}/{}.txt".format(dirname, t), 'r') as f:
                tmp = set(f.read().split())

            if len(links) == 0:
                links = tmp
            else:
                links = links.intersection(tmp)


        with open(fname, 'w') as f:
            for l in links:
                f.write("{}\n".format(l))
                doc_count += 1


        print("{} links written to {}".format(doc_count, fname))


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("USAGE: python retriever.py <term>")
        exit()

    retrieve(sys.argv[1:])
