import re
import json
import nltk
import time
import string
import os.path
from math import log
from pprint import pprint
from HTMLParser import HTMLParser
from collections import defaultdict
from htmlentitydefs import name2codepoint


#####################
# CLASS DEFINITIONS #
#####################

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.increase_weight = False
        self.end_tag = None
        self.title = True # true if not inside a body tag (see additional information pdf for why...)


    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.title = False

        if tag == 'b' or re.match(r'h\d',tag) or tag == 'strong':
            self.increase_weight = True

        for attr in attrs:
            if attr[0] == 'style' and re.match(r'font-weight:\s?bold',attr[1]):
                self.end_tag = tag


    def handle_endtag(self, tag):
        if tag == 'b' or re.match(r'h\d',tag) or tag == 'strong':
            self.increase_weight = False

        if tag == self.end_tag:
            self.end_tag = None

        if tag == 'body':
            self.title = True #not in body anymore

            #if we reach the end of a body reset the other flags
            self.end_tag = None
            self.increase_weight = False


    def handle_data(self, data):

        global index
        tokens = re.split('[^a-zA-Z0-9]', data)

        for t in tokens:
            if t: # Ignore empty string
                t = t.lower()
                if self.title:
                    index[t][curr_docid] += 4
                elif self.increase_weight or self.end_tag != None:
                    index[t][curr_docid] += 2
                else:
                    index[t][curr_docid] += 1
                docs.add(curr_docid)


####################
# GLOBAL VARIABLES #
####################

docs = set()
curr_docid = ""
parser = MyHTMLParser()
printable = set(string.printable)
index = defaultdict(lambda : defaultdict(int))


#############
# FUNCTIONS #
#############

# http://stackoverflow.com/questions/26496831/how-to-convert-defaultdict-of-defaultdicts-of-defaultdicts-to-dict-of-dicts-o
def defaultdict_to_dict(d):
    if isinstance(d, defaultdict):
        d = {k: defaultdict_to_dict(v) for k, v in d.iteritems()}
    return d


def tf_idf(term, docid):
    if docid not in index[term]:
        return 0
    return log(1+index[term][docid], 10)*log(len(docs)/len(index[term]), 10)


def index_doc(d, f):
    global curr_docid
    curr_docid = "{}/{}".format(d, f)
    fname = "WEBPAGES_CLEAN/{}".format(curr_docid)

    if not os.path.isfile(fname):
        return

    with open(fname, 'r') as infile:
        contents = infile.read()

    parser.feed(contents)


def write_index_to_file(file="index.txt"):
    with open(file, 'w') as f:
        d = defaultdict_to_dict(index)
        for term,docs in index.iteritems():
            for doc,count in docs.iteritems():
                d[term][doc] = tf_idf(term,doc)
        f.write(json.dumps(d))


########
# MAIN #
########

if __name__ == "__main__":

    start = time.time()

    # Decrease these nums to use fewer files for testing
    num_dirs = 75
    num_files = 500

    for d in range(num_dirs):
        for f in range(num_files):
            index_doc(d, f)

    write_index_to_file()

    print("Number of documents: {}".format(len(docs)))
    print("Number of unique words: {}".format(len(index)))
    print("Time elapsed: {}".format(time.time() - start))

