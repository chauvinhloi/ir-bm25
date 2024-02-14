from src.finder import Finder
from helpers import xml_process
import sys
import getopt
import time
import re


def main(argv):
    # ============================================================
    # Parsing arguments
    help_text = """Please use the following syntax: python search.py -f <similarity_function> -q <query_label> \
-n <num_results> -l <lexicon> -i <invlists> -m <map> -s <stoplists> -t <query_terms> """
    sim_function = ''
    query_label = ''
    num_results = ''
    lexicon_path = ''
    invlists_path = ''
    map_path = ''
    stoplist_path = ''
    query = ''
    try:
        opts, args = getopt.getopt(argv, "hf:q:n:l:i:m:s:t:", [
            "function=", "querylabel=", "numresults=",
            "lexicon=", "invlists=", "map=", "stoplist=", "queryterms="])
    except getopt.GetoptError:
        print help_text
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print help_text
            sys.exit()
        elif opt in ("-f", "--simfunc"):
            sim_function = arg
        elif opt in ("-q", "--qlabel"):
            query_label = arg
        elif opt in ("-n", "--nresults"):
            num_results = int(arg)
        elif opt in ("-l", "--lexicon"):
            lexicon_path = arg
        elif opt in ("-i", "--invlists"):
            invlists_path = arg
        elif opt in ("-m", "--map"):
            map_path = arg
        elif opt in ("-s", "--stoplist"):
            stoplist_path = arg
        elif opt in ("-t", "--qterms"):
            q = re.match(r".*-t\s([A-Za-z ]*)-?", ' '.join(argv))
            query = q.group(1).strip()

    start = time.time()

    # ============================================================
    # Create Finder
    finder = Finder(lexicon_path, map_path, invlists_path)

    # ============================================================
    # Process Query
    stopwords_file = open(stoplist_path, 'r')
    stopwords = stopwords_file.read().split()
    stopwords_file.close()
    query_terms = xml_process.prettify(query).split(' ')
    query_terms = [term for term in query_terms if term not in stopwords]

    # ============================================================
    # Performing Search
    results = finder.search(query_terms, sim_function, num_results)

    # ============================================================
    # Output results
    for i, result in enumerate(results):
        doc_id = result[0]
        score = result[1]
        print(query_label + ' ' + finder.get_doc_no(doc_id) + ' ' + str(i + 1) + ' ' + str(score))

    end = time.time()
    print("Running time: " + str(round((end - start)*1000, 0)) + " ms")


if __name__ == "__main__":
    main(sys.argv[1:])
