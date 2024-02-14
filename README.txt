Information Retrieval BM25


=========================================================
Indexing document
=========================================================

Note: All the search functions below will only work with the files generated from this indexing function.
For simplicity, the index files can be download at:
https://www.dropbox.com/s/edq5foqnnac5dba/indexfiles.zip?dl=0

Type python index.py -h to view all available arguments.

Arguments:
-s <stop_list>: path to stop list
-f <source_file>: path to source file

Example:
python index.py -s ./data/stoplist -f ./data/latimes

Results:
File Loading:
Number of documents: 131896
1.35700011253

Mapper:
[======                                                               7%]

The approximate time for completion of indexing is 10 minutes. Please consider downloading the provided index files for
convenient.

=========================================================
Using basic search
=========================================================

Type python search.py -h to view all available arguments.

Arguments:
-f <similarity_function>: similarity function to use, only BM25 is supported
-q <query_label>: label for query job
-n <num_results>: number of results to be returned
-l <lexicon>: path to lexicon file
-i <invlists>: path to inverted list file
-m <map>: path to map file
-s <stoplists>: path to stop list
-t <query_terms>: list of query terms

Example:
python search.py -f BM25 -q test -n 20 -l ./lexicon.txt -i ./invlists.bin -m ./map.txt -s ./data/stoplist -t window made in australia

Results:
test LA121190-0039 1 11.92844
test LA072390-0060 2 11.78297
test LA031289-0074 3 11.46136
test LA102789-0129 4 10.68328
test LA080689-0024 5 10.42197
test LA030490-0048 6 10.33173
test LA082889-0078 7 9.98137
test LA101989-0234 8 9.86186
test LA061789-0083 9 9.56933
test LA052489-0156 10 9.49488
test LA092489-0059 11 9.27522
test LA121089-0077 12 9.25361
test LA101990-0109 13 9.21415
test LA070190-0213 14 8.95879
test LA062589-0005 15 8.94271
test LA060790-0093 16 8.91549
test LA102189-0131 17 8.91385
test LA081489-0061 18 8.90229
test LA090890-0155 19 8.88639
test LA101589-0099 20 8.8807

=========================================================
Using advanced search
=========================================================

Type python advanced_search.py -h to view all available arguments.

Arguments:
-f <similarity_function>: similarity function to use, only BM25 is supported for now.
-q <query_label>: label for query job
-n <num_results>: number of results to be returned
-l <lexicon>: path to lexicon file
-i <invlists>: path to inverted list file
-m <map>: path to map file
-d <doc>: path to orginal document file
-s <stoplists>: path to stop list
-r <nrelevance>: number of relevant documents
-e <nexpansion>: number of words to be added into the original query
-t <query_terms>: list of query terms

Example:
python advanced_search.py -f BM25 -q 402 -n 20 -l ./lexicon.txt -i ./invlists.bin -m ./map.txt -d ./data/latimes -s ./data/stoplist -r 10 -e 20 -t behavioral genetics

Results:
402 LA101290-0115 1 103.25274
402 LA080190-0099 2 93.43924
402 LA042990-0032 3 92.73881
402 LA052290-0110 4 76.1725
402 LA121289-0055 5 69.93483
402 LA073090-0057 6 65.22648
402 LA032290-0148 7 63.85232
402 LA062590-0042 8 60.37681
402 LA020789-0112 9 60.03141
402 LA071689-0143 10 54.5821
402 LA062890-0104 11 53.69662
402 LA020389-0077 12 53.40113
402 LA082590-0108 13 53.28666
402 LA121589-0077 14 53.22266
402 LA060289-0090 15 52.75694
402 LA121790-0086 16 52.41038
402 LA011089-0045 17 52.40229
402 LA090189-0093 18 51.69423
402 LA020789-0113 19 51.58559
402 LA072490-0082 20 51.41043

