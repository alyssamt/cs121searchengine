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


'''
TO-DO:

Words in bold and in heading (h1, h2, h3) should be treated as more important than the other
words. You can handle this as you want: create separate indexes, or add metadata about the words
to the single index.
'''


#####################
# CLASS DEFINITIONS #
#####################

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        #print "Start tag:", tag
        for attr in attrs:
            pass #print "     attr:", attr

    def handle_endtag(self, tag):
        pass #print "End tag  :", tag

    def handle_data(self, data):

        global index

        #print "Data     :", data

        tokens = re.split('[^a-zA-Z0-9]', data)
        #data = filter(lambda x: x in printable, data)
        #tokens = nltk.word_tokenize(data)

        #print(tokens)
        
        for t in tokens:
            if t: # Ignore empty string
                t = t.lower()
                index[t][curr_docid] += 1
                docs.add(curr_docid)

    def handle_comment(self, data):
        pass #print "Comment  :", data

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        #print "Named ent:", c

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        #print "Num ent  :", c

    def handle_decl(self, data):
        pass #print "Decl     :", data


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

    #print("\nDOCUMENT {}/{}".format(d, f))
    #print(contents)

    parser.feed(contents)

    #for word in index:
    #    print("{}: {}".format(word, dict(index[word])))


def write_index_to_file(file="index.txt"):
    
    with open(file, 'w') as f:
        d = defaultdict_to_dict(index)
        f.write(json.dumps(d))


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

