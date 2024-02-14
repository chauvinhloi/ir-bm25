from src.indexer import Indexer
from helpers import progress, file_util
import os
import sys
import getopt
import time


def main(argv):
    # ============================================================
    # Parsing arguments
    help_text = "Please use the following syntax: python index.py -s <stop_list> -f <source_file>"
    doc_path = ''
    stopwords_path = ''
    try:
        opts, args = getopt.getopt(argv, "hs:f:", ["stoplist=", "file="])
    except getopt.GetoptError:
        print help_text
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print help_text
            sys.exit()
        elif opt in ("-s", "--stoplist"):
            stopwords_path = arg
        elif opt in ("-f", "--file"):
            doc_path = arg

    if len(doc_path) == 0:
        print help_text
        sys.exit(2)
    # ============================================================
    # Create indexer
    indexer = Indexer()

    # ============================================================
    # Open document
    start = time.time()
    print('File Loading: ')

    documents, ndocs = file_util.read_docs(doc_path, '</DOC>')
    print('Number of documents: ' + str(ndocs))
    end = time.time()
    print(end - start)

    # ============================================================
    # Run mapper
    print('')
    start = time.time()
    print('Mapper: ')

    if len(stopwords_path) > 0:
        stopwords_file = open(stopwords_path, 'r')
        stopwords = stopwords_file.read().split()
        stopwords_file.close()
        for doc_sequence, document in enumerate(documents):
            progress.run(doc_sequence, ndocs)
            indexer.run_mapper(doc_sequence, document, stopwords)
    else:
        for doc_sequence, document in enumerate(documents):
            progress.run(doc_sequence, ndocs)
            indexer.run_mapper(doc_sequence, document)

    end = time.time()
    print('\n' + str(end - start))

    # ============================================================
    # Run reducer
    print('')
    start = time.time()
    print('Reducer: ')

    indexer.run_reducer()

    end = time.time()
    print('\n' + str(end - start))

    # ============================================================
    # Dump artifacts
    print('')
    start = time.time()
    print('Writing files, please wait... ')

    indexer.dump_map('./map.txt')  # map file
    indexer.dump_lexicon('./lexicon.txt')  # lexicon
    indexer.dump_inv_index('./invlists.bin', file_type='bin')  # inverted index

    end = time.time()
    print(end - start)

    # ============================================================
    # Clean up
    print('')
    print('Cleaning up, please wait...')
    cache = './src/.cache/'
    for f in [os.path.join(cache, f) for f in os.listdir(cache)]:
        os.remove(f)
    print('Finished!')


if __name__ == "__main__":
    main(sys.argv[1:])
