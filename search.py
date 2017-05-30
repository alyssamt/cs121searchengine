import os

from retriever import retrieve

####################
# GLOBAL VARIABLES #
####################

terminate_terms = set(['exit','q','quit','qq','bye','goodbye'])
links_dir = 'retrieved_links/'

#############
# FUNCTIONS #
#############

def should_terminate(command):
    return command in terminate_terms

def get_links(query):
    links = []
    try:
        print query.replace(' ','_')+'.txt'
        with open(links_dir+query.replace(' ','_')+'.txt','r') as link_file:
            for line in link_file:
                links.append(line)
        return links
    except IOError:
        retrieve(query.split())
        return get_links(query)

if __name__ == '__main__':
    c = None
    os.system('indexer.py')
    c = raw_input('Enter a search term (q to quit):')
    while not should_terminate(c):
        print ''
        if should_terminate(c):
            break

        i = 0
        for link in get_links(c):
            print link
            i += 1
            if i % 10 == 0:
                cont = raw_input('press return to continue... (s to exit search)')
                if cont != '':
                    break

        print '\n'
        c = raw_input('Enter a search term:')









    print '\n#############\n# Goodbye!! #\n#############\n'
