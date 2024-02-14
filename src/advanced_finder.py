from src.finder import Finder
from src.indexer import Indexer
import numpy as np
from math import log
from helpers import file_util
import time
import re


class AdvancedFinder(Finder, Indexer):
    """
    Advanced Finder class inherit Finder and Indexer classes
    """
    def __init__(self, lexicon_path, map_path, invlists_path, doc_path, stopwords_path):
        Finder.__init__(self, lexicon_path, map_path, invlists_path)
        self.lexicon_vector = sorted(self.lexicon.keys())  # Lexicon vector used for vectorising documents
        self.documents, self.total_ndocs = file_util.read_docs(doc_path, '</DOC>')  # Read and split documents
        stopwords_file = open(stopwords_path, 'r')
        self.stopwords = stopwords_file.read().split()  # Getting stop words from file
        stopwords_file.close()

    def get_doc(self, doc_id):
        # Method to get document by its id
        return self.documents[doc_id]

    def vectorize(self, document):
        # Convert document into vector
        word_freq = dict()
        tokens = self.parse(None, document, build_map=False)  # No need to update map
        tokens = self.remove_stop_words(tokens, self.stopwords)  # Remove stop words

        # Word count
        for token in tokens:
            token = file_util.auto_conv(token)
            word_freq[token] = word_freq.get(token, 0) + 1

        # Return a vactor
        vect = [word_freq.get(word, 0) for word in self.lexicon_vector]
        return vect

    def idf(self, ndocs, term, doc_ids):
        # Calculating IDF of given term in a list of documents
        doc_freq, pointer = self.lexicon_lookup(term)
        postings = self.get_postings(doc_freq, pointer)  # Get posting list from inverted list file
        doc_freq = 0
        i = 0
        while i < len(postings):
            doc_id = postings[i]
            if doc_id in doc_ids:
                doc_freq = doc_freq + 1
            i = i + 2

        return log((ndocs - doc_freq + 0.5)/(doc_freq + 0.5))

    def query_expand(self, r, e, top_rel_ids, query_terms, tfk=1.2):
        # Get top r in list of relevant documents
        doc_ids = top_rel_ids[:r]

        # Vectorize documents
        doc_vectors = np.array([self.vectorize(self.get_doc(doc_id)) for doc_id in doc_ids])

        # IDF vector
        idf = np.sum(1*(doc_vectors > 0), axis=0)

        # TF-IDF transform
        transformed_vectors = []
        for a in doc_vectors:
            transformed_vectors.append((tfk + 1)*a*idf/(tfk + a))

        # Getting average vector
        avg_vector = np.mean(transformed_vectors, axis=0)

        # Get top terms to be included in new query
        new_query_terms = query_terms
        for k, v in sorted(dict(zip(self.lexicon_vector, avg_vector)).items(), key=lambda x: x[1], reverse=True)[:e]:
            new_query_terms.append(k)

        return new_query_terms
