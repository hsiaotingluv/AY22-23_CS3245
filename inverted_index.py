import os
from sys import platform
import shutil
import string
import time

from queue import PriorityQueue
from math import sqrt
from math import ceil, floor
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer

class InvertedIndex:
    MAX_LINES_IN_MEM = 10000

    def __init__(self, in_dir, out_dict, out_postings):
        print("initialising inverted index...")

        self.in_dir = in_dir
        self.out_dict = out_dict
        self.out_postings = out_postings
    
    def construct(self):
        print("constructing index...")

        stemmer = PorterStemmer()
        stop_words = set(stopwords.words('english'))
        remove_punctuation = str.maketrans('', '', string.punctuation)
        remove_digit = str.maketrans("", "", string.digits)

        block_index = 0
        mem_line = 0
        curr_doc_num = 0
        total_doc_num = 1

        all_doc_ids = []
        for doc_id in os.listdir(self.in_dir):
            if (curr_doc_num == total_doc_num):
                break
            else:
                all_doc_ids.append(int(doc_id))
                curr_doc_num += 1
        all_doc_ids.sort()

        print("all doc id: ", all_doc_ids)

        terms = list()
        postings = {} # key: term, value: list of doc_id

        for doc_id in all_doc_ids:
            doc_id = str(doc_id)
            file = open(os.path.join(self.in_dir, doc_id))
            for line in file:
                for sentence_token in sent_tokenize(line):
                    for word_token in word_tokenize(sentence_token):
                        # ignore if number
                        if word_token.isnumeric():
                            continue

                        # remove punctuation and digit, stem and case-folding
                        word_token = stemmer.stem(word_token.translate(remove_punctuation).translate(remove_digit)).lower()

                        if len(word_token) == 0:
                            continue

                        # add word_token into list of terms
                        if word_token not in terms:
                            print("word token not in terms")
                            terms.append(word_token)
                            mem_line += 1

                            print("mem line: ", mem_line)

                        # add word_token into posting list
                        if word_token not in postings:
                            print("word token not in posting")
                            postings[word_token] = list()
                            postings[word_token].append(doc_id)
                        else :
                            if doc_id not in postings[word_token]:
                                print("add doc_id: ", doc_id)
                                postings[word_token].append(doc_id)

                        
                        if mem_line == self.MAX_LINES_IN_MEM:
                            terms.sort()
                            self.write_block_to_disk(block_index, terms, postings)
                            print("Block " + str(block_index) + " created")
                            
                            mem_line = 0
                            block_index += 1
                            terms = list()
                            postings = {} # key: term, value: list of doc_id

        # print("terms: ", terms)
        # print("postings: ", postings)
    
        if mem_line > 0:
            terms.sort()
            self.write_block_to_disk(block_index, terms, postings)
            # print("sorted terms: ", terms)
            print("adding remaining lines...")
            # merge_blocks()
        else:
            # merge_blocks()
            print("no remaining line...")
        
    def write_block_to_disk(self, block_index, terms, postings):
        print("terms write block to disk: ", terms)
        result = ""
        if terms is not None:
            print("writing terms...")
            for term in terms:
                posting = ' '.join(str(i) for i in postings[term])
                result += term + " " + posting + "\n"

            print("terms: ", terms)
            print("postings: ", postings)

            f = open("block_" + str(block_index) + ".txt", "w")
            f.write(result)
            f.close()





    
