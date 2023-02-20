import os
from sys import platform
import shutil
import string
import time

from queue import PriorityQueue
from math import sqrt, floor
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import PorterStemmer

class InvertedIndex:
    # max 10000 number of terms in memory
    # TODO: check how to set max memory
    MAX_LINES_IN_MEM = 10000

    def __init__(self, in_dir, out_dict, out_postings):
        # print("initialising inverted index...")

        self.in_dir = in_dir
        self.out_dict = out_dict
        self.out_postings = out_postings
    
    def get_all_doc_ids(self):
        curr_doc_num = 0
        total_doc_num = 7770

        all_doc_ids = []
        for doc_id in os.listdir(self.in_dir):
            if (curr_doc_num == total_doc_num):
                break
            else:
                all_doc_ids.append(int(doc_id))
                curr_doc_num += 1
        all_doc_ids.sort()

        # print("all doc id: ", all_doc_ids)

        return all_doc_ids
    
    def construct(self):
        # print("deleting previous test files...")
        self.delete_test_files

        if not os.path.exists("blocks"):
            os.makedirs("blocks")

        # print("constructing index...")

        stemmer = PorterStemmer()
        stop_words = set(stopwords.words('english'))
        remove_punctuation = str.maketrans('', '', string.punctuation)
        remove_digit = str.maketrans("", "", string.digits)

        block_index = 0
        mem_line = 0
        all_doc_ids = self.get_all_doc_ids()
        terms = list()
        postings = {} # key: term, value: list of doc_id

        for doc_id in all_doc_ids:
            doc_id = str(doc_id)
            file = open(os.path.join(self.in_dir, doc_id))
            for line in file:
                for sentence_token in sent_tokenize(line):
                    for word_token in word_tokenize(sentence_token):
                        # remove punctuation and digit, stem and case-folding
                        word_token = stemmer.stem(
                            word_token.translate(remove_punctuation).translate(remove_digit)).lower()

                        # remove numbers, stop words or empty strings
                        if word_token.isnumeric() or word_token in stop_words or len(word_token) == 0:
                            continue

                        # add word_token into list of terms
                        if word_token not in terms:
                            # print("word token not in terms")
                            terms.append(word_token)
                            mem_line += 1

                            # print("mem line: ", mem_line)

                        # add word_token into posting list
                        if word_token not in postings:
                            # print("add word token into posting")
                            postings[word_token] = list()
                            postings[word_token].append(doc_id)
                        else :
                            if doc_id not in postings[word_token]:
                                # print("add new doc_id into posting: ", doc_id)
                                postings[word_token].append(doc_id)

                        # if max lines in mem reached, write block to disk
                        if mem_line == self.MAX_LINES_IN_MEM:
                            terms.sort()
                            self.write_block_to_disk(block_index, terms, postings)
                            # print("Block " + str(block_index) + " created")
                            
                            mem_line = 0
                            block_index += 1
                            terms = list()
                            postings = {} # key: term, value: list of doc_id
    
        if mem_line > 0:
            terms.sort()
            self.write_block_to_disk(block_index, terms, postings)
            # print("adding remaining lines...")
            self.merge_blocks(block_index + 1)
        else:
            self.merge_blocks(block_index)
            # print("no remaining line...")
        
    def write_block_to_disk(self, block_index, terms, postings):
        # print("terms write block to disk: ", terms)
        result = ""
        if terms is not None:
            # print("writing terms...")
            for term in terms:
                posting = ' '.join(str(i) for i in postings[term])
                result += term + " " + posting + "\n"

            # print("terms: ", terms)
            # print("postings: ", postings)

            f = open(os.path.join("blocks", "block_" + str(block_index) + ".txt"), "w")
            f.write(result)
            f.close()
    
    def merge_blocks(self, total_num_blocks):
        # print("merging ", total_num_blocks, " numbers of blocks...")
        
        # off set of start line for each block
        start_offset_per_block = [0] * total_num_blocks
        # lines loaded from each block
        line_in_mem_per_block = [0] * total_num_blocks
        # total number of lines loaded from each block at each time
        lines_to_read = max(1, floor(self.MAX_LINES_IN_MEM / total_num_blocks))
        # item = [term, postings, block_index]
        queue = PriorityQueue() 
        
        # load first set of lines from all blocks and add to queue
        for block_index in range (0, total_num_blocks):
            newLines_list = self.read_block(block_index, start_offset_per_block, lines_to_read)
            queue = self.add_list_to_queue(newLines_list, line_in_mem_per_block, block_index, queue)
            
            # print("start offset per block: ", start_offset_per_block)
            # print("line in mem per block: ", line_in_mem_per_block)

        prev_term = ""
        accumulated_postings = []
        final_dictionary = "" # term freq reference
        final_postings = "" # term docIDs...
        posting_ref = 0
        line_in_mem = 0
        last_unique_term = False

        while not queue.empty():
            item = queue.get()
            curr_term = item[0]
            curr_postings = item[1].split()
            curr_block_index = item[2]
            # print("curr item: ", item)

            line_in_mem_per_block[curr_block_index] -= 1

            # append same term together
            if (prev_term == "" or prev_term == curr_term):
                # print("appending same term together...")
                # print("current term: ", curr_term)
                # print("previous term: ", prev_term)

                prev_term = curr_term
                for doc_id in curr_postings:
                    if doc_id not in accumulated_postings:
                        accumulated_postings.extend(curr_postings)
                # print("accumulated posting: ", accumulated_postings, " for term ", curr_term)

            # if new term, append previous term to final dictionary and postings
            if (curr_term != prev_term):
                # print("appending to final dictionary and postings...")
                # print("queue is empty: ", queue.empty())
                # print("accumulated posting: ", accumulated_postings, " for term ", prev_term)

                new_dictionary_posting_line = self.new_line(prev_term, accumulated_postings, posting_ref)
                final_dictionary += new_dictionary_posting_line[0]
                final_postings += new_dictionary_posting_line[1]
                posting_ref += len(new_dictionary_posting_line[1])
                line_in_mem += 1

                # reset values
                prev_term = curr_term
                accumulated_postings = curr_postings

                if (queue.empty()):
                    last_unique_term = True

                # print("final dictionary: ", final_dictionary)
                # print("final postings: ", final_postings)
                
            # load another set of lines into queue
            if (line_in_mem_per_block[curr_block_index] == 0):
                # print("loading ", str(lines_to_read), " lines from block ", str(curr_block_index), "...")

                newLines_list = self.read_block(curr_block_index, start_offset_per_block, lines_to_read)
                queue = self.add_list_to_queue(newLines_list, line_in_mem_per_block, curr_block_index, queue)

                # print("start offset per block: ", start_offset_per_block)
                # print("line in mem per block: ", line_in_mem_per_block)

            # write out into dictionary and postings file
            if (line_in_mem == self.MAX_LINES_IN_MEM):
                # print("writing to output files...")
                self.write_block(self.out_dict, final_dictionary)
                self.write_block(self.out_postings, final_postings)

                # reset values
                line_in_mem = 0
                final_dictionary = "" 
                final_postings = ""

        # append last unique term to final dictionary and postings
        if (last_unique_term):
            new_dictionary_posting_line = self.new_line(curr_term, curr_postings, posting_ref)
            final_dictionary += new_dictionary_posting_line[0]
            final_postings += new_dictionary_posting_line[1]

        # write out into final dictionary and postings
        # print("writing to output files...")
        self.write_block(self.out_dict, final_dictionary)
        self.write_block(self.out_postings, final_postings)

    # read and return lines_to_read number of lines in block with block_index
    def read_block(self, block_index, start_offset_per_block, lines_to_read):
        # f = open(os.path.join("blocks", "block_" + str(block_index) + ".txt"), "w")
        block_path = os.path.join(os.getcwd(), "blocks")
        start_line = start_offset_per_block[block_index]

        f = open(os.path.join(block_path, "block_" + str(block_index) + ".txt"), 'r')
        # f = open("block_" + str(block_index) + ".txt", "r")
        f.seek(start_line)
        lines = []

        # read from line number start_line to (start_line + lines_to_read - 1)
        for i in range (0, lines_to_read):
            line = f.readline().strip()
            if len(line) == 0:
                break
            lines.append(line)
        
        start_offset_per_block[block_index] = f.tell() + 1 # add 1 for "\n"
        
        f.close()
        # print("lines read: ", lines)
            
        return lines

    def write_block(self, out_file, content):
        f = open(out_file, "a")
        f.write(content)
        f.close()

    # TODO: function does not work as expected
    def delete_test_files(self):
        shutil.rmtree("blocks")
        os.remove("dictionary.txt")
        os.remove("postings.txt")

    def add_list_to_queue(self, newLines_list, line_in_mem_per_block, block_index, queue):
        for line in newLines_list:
                line_in_mem_per_block[block_index] += 1
                term_postings = line.split(" ", 1)
                term = term_postings[0]
                postings = term_postings[1]
                # print("added to queue: ", [term, postings, block_index]) 
                queue.put([term, postings, block_index])
        return queue
    
    def new_line(self, prev_term, accumulated_postings, posting_ref):
        # term freq posting_ref
        new_dictionary_line = prev_term + " " + str(len(accumulated_postings)) + " " + str(posting_ref) + "\n"
    
        # term DocIDs...
        postings_with_skip_pointers = self.get_postings_with_skip_pointers(accumulated_postings)
        new_posting_line = prev_term + " " + postings_with_skip_pointers + "\n"

        return [new_dictionary_line, new_posting_line]
    
    def get_postings_with_skip_pointers(self, accumulated_postings):
        # print("getting skip pointers...")

        length = len(accumulated_postings)
        min_skip_length = 9

        # do not add skip pointers if length of postings is smaller than min_skip_length
        if (length < min_skip_length):
            return ' '.join(accumulated_postings)

        postings_with_skip_pointers = ""
        skip_len = floor(sqrt(length))

        for i in range (0, length):
            if (i % skip_len == 0):
                postings_with_skip_pointers += accumulated_postings[i] + "| "
            else:
                postings_with_skip_pointers += accumulated_postings[i] + " "

        return postings_with_skip_pointers
