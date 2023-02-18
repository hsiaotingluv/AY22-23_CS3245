#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

# TODO
def write_block(dict, out_postings):
    x = 0

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below

    # Implementation of SPIMI

    ps = PorterStemmer()
    dictionary = {} 
    block_limit = 50

    for doc_id in os.listdir(in_dir): 
        f = open(os.path.join(in_dir, doc_id), "r")
        file = f.read()
        words = word_tokenize(file)

        # Step 1: Generate an index as the pairs are processed
        for word in words:

            """
            - Stem the word and add it to the dictionary + posting list
            - Go as far as memory allows, write out the index and then merge later; For this assignment, set an artifical block size. 
            """
            stemmed_word = ps.stem(word)

            # 1.1 Create hash and consolidate terms
            if dictionary.get(stemmed_word) == None:
                dictionary[stemmed_word] = [int(doc_id)]

            else: 
                # Avoid duplicate docIDs for one term
                if dictionary[stemmed_word].count(int(doc_id)) == 0: 
                    dictionary[stemmed_word].append(int(doc_id))

            # If block (artificial memory) is full, write to disk
            if len(dictionary) == block_limit:
                write_block(dictionary, out_postings)
                # Reset memory
                dictionary = {}

    # Write final block
    if len(dictionary) > 0:
        write_block(dictionary, out_postings) 

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
