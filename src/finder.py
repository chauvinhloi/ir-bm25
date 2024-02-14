from helpers import file_util
from math import log


class Finder:
    """
    Searching for terms in corpus
    """
    def __init__(self, lexicon_path, map_path, invlists_path):
        self.docs_map = file_util.import_dict(map_path)
        self.lexicon = file_util.import_dict(lexicon_path)
        self.invlists_path = invlists_path
        self.num_docs = len(self.docs_map)
        self.avdl = self.get_avdl()
        self.results = dict()

    def lexicon_lookup(self, term):
        # Get doc frequency and pointer to invlist
        value = self.lexicon.get(term, None)
        if value is not None:
            doc_freq = value[0]
            pointer = value[1]
            return doc_freq, pointer
        else:
            return None, None

    def get_postings(self, doc_freq, pointer):
        # Get posting list from inverted list file
        return file_util.read_bin(self.invlists_path, pointer, doc_freq)

    def get_doc_no(self, doc_id):
        # Method to get document number by its id
        return self.docs_map[doc_id][0]

    def get_avdl(self):
        # Calculating average document length for length normalisation
        total_len = sum([v[1] for k, v in self.docs_map.items()])
        return round(total_len/self.num_docs, 5)

    def bm25(self, ndocs, term_freq, doc_freq, doc_len, avdl, k1=1.2, b=0.75):
        # Okapi BM25 score calculation for one term
        k = k1*((1 - b) + b*doc_len/avdl)
        bm25 = log((ndocs - doc_freq + 0.5)/(doc_freq + 0.5))*((k1 + 1)*term_freq/(k + term_freq))
        return round(bm25, 5)

    def term_search(self, term, sim_func="BM25"):
        if sim_func == "BM25":
            doc_freq, pointer = self.lexicon_lookup(term)
            if doc_freq is not None:
                postings = self.get_postings(doc_freq, pointer)
                i = 0

                while i < len(postings):
                    doc_id = postings[i]
                    term_freq = postings[i + 1]
                    doc_len = self.docs_map[doc_id][1]
                    score = self.bm25(self.num_docs, term_freq, doc_freq, doc_len, self.avdl)
                    # Update document similarity score for one term
                    self.results[doc_id] = self.results.get(doc_id, 0.0) + score
                    i = i + 2

    def search(self, query_terms, sim_func, num_results):
        # Construct table of document similarity score
        for term in query_terms:
            self.term_search(term, sim_func)
        # Sorting and get top results
        results = sorted(self.results.items(), key=lambda x: x[1], reverse=True)[:num_results]
        return results

