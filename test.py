from src.advanced_finder import AdvancedFinder

advanced_finder = AdvancedFinder('./lexicon.txt', './map.txt', './invlists.bin', './data/latimes', '</DOC>')

stopwords_file = open('./data/stoplist', 'r')
stopwords = stopwords_file.read().split()
stopwords_file.close()

advanced_finder.doc_partitioning(0, "equi-freq", stopwords, k=10)
