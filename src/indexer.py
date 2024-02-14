from helpers import xml_process
from helpers import file_util
from helpers import progress
import os
import ntpath


class Indexer:
    """
    Constructing Inverted Index
    """
    def __init__(self):
        self.docs_map = dict()
        self.lexicon = dict()
        self.inv_index = dict()
        self.sorted_inv_index = []

    def parse(self, doc_id, document, build_map=True):
        doc_no = xml_process.extract_from_tag(document, 'DOCNO')
        if build_map:
            self.docs_map.update({doc_id: (doc_no, 0)})
        headlines = xml_process.extract_from_tag(document, 'HEADLINE')
        text = xml_process.extract_from_tag(document, 'TEXT')
        text = xml_process.prettify(text)
        headlines = xml_process.prettify(headlines)
        content = headlines + ' ' + text
        return content.split()

    @ staticmethod
    def remove_stop_words(tokens, stopwords):
        return [token for token in tokens if token not in stopwords]

    def run_mapper(self, doc_id, document, stopwords=None):
        tokens = self.parse(doc_id, document)

        if stopwords is not None:
            tokens = self.remove_stop_words(tokens, stopwords)

        doc_no = self.docs_map[doc_id][0]
        self.docs_map.update({doc_id: (doc_no, len(tokens))})
        words_count = dict()

        # Local count
        for token in tokens:
            words_count[token] = words_count.get(token, 0) + 1

        # Dump to disk
        this_folder = os.path.dirname(os.path.realpath(__file__))
        cache_file = os.path.join(this_folder + '/.cache/', str(doc_id) + '.txt')
        with open(cache_file, 'w+') as f:
            for word, count in words_count.items():
                f.write(word + ' ' + str(count) + '\n')

    def run_reducer(self):
        this_folder = os.path.dirname(os.path.realpath(__file__))
        cache_path = os.path.join(this_folder + '/.cache/')
        files_list = sorted([int(ntpath.basename(f).split('.')[0]) for f in os.listdir(cache_path)])
        nfiles = len(files_list)
        # Constructing inverted list in memory
        for i, fname in enumerate(files_list):
            progress.run(i, nfiles)
            fpath = os.path.join(cache_path, str(fname) + '.txt')
            doc_id = fname

            for line in open(fpath, "r"):
                content = line.split()
                term = content[0]
                term_freq = int(content[1])

                # Update posting list
                posting_list = self.inv_index.get(term, None)
                if posting_list is None:
                    self.inv_index.update({term: [(doc_id, term_freq)]})
                else:
                    self.inv_index[term].append((doc_id, term_freq))
        # Sort
        self.sorted_inv_index = sorted(self.inv_index.items())

        # Constructing lexicon in memory
        pointer = 0
        nindex = len(self.sorted_inv_index)
        i = 0
        print('')
        for k, v in self.sorted_inv_index:
            progress.run(i, nindex)
            self.lexicon.update({k: (len(v), pointer)})
            pointer = pointer + 2*len(v)
            i = i + 1

    def dump_map(self, map_path):
        with open(map_path, 'w+') as f:
            for k, v in self.docs_map.items():
                f.write(str(k) + ' ' + str(v[0]) + ' ' + str(v[1]) + '\n')

    def dump_lexicon(self, lexicon_path):
        with open(lexicon_path, 'w+') as f:
            for k, v in sorted(self.lexicon.items()):
                f.write(str(k) + ' ' + str(v[0]) + ' ' + str(v[1]) + '\n')

    def dump_inv_index(self, inv_index_path, file_type='text'):
        if file_type == 'text':
            with open(inv_index_path, 'w+') as f:
                for k, v in self.sorted_inv_index:
                    f.write(str(k))
                    for pair in v:
                        f.write(' ' + str(pair[0]) + ' ' + str(pair[1]))
                    f.write('\n')
        if file_type == 'bin':
            file_util.write_bin(inv_index_path, self.sorted_inv_index)

