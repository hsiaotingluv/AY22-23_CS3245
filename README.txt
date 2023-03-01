This is the README file for A0222182R's submission
Email(s): e0559714@u.nus.edu

== Python Version ==

I'm (We're) using Python Version <3.10.9> for this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

###Description
This program implements indexing and searching techniques for Boolean retrieval from a set of training data given to it. It is capable of finding all docIDs in the training data that satisfy all the conditions stated in the Boolean retrieval. 

###How to use
To build the indexing script, index.py, run:
$ python3 index.py -i directory-of-documents -d dictionary-file -p postings-file
which will store your dictionary into dictionary-file and postings into postings-file.

To run the searching script, search.py, run:
$ python3 search.py -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results
which will store the queries results into output-file-of-results.

###About Indexing
We created a InvertedIndex class that leverages on the SPIMI algorithm to help with the indexing of all documents. 

###About construct
####Tokenisation
First, we obtain a sorted list of all document ids. Then, we construct the index by looping through each document id and tokenising every term in each document. The tokenisation of term is done using a series of techniques such as removing punctuation and digits, as well as stemming and case folding. To further optimise space, we also remove numbers or empty strings. 

####Block
After tockenising every term, we add the term into a list of term, and the document id into posting, only if they are not previously added. When the number of terms reaches MAX_LINES_IN_MEM, which we decided on the value of 10,000, the program sorts all the current unique terms, and write the terms and their postings into a block. It then repeats the cycle, continuously creating more blocks, until all terms from all documents are stored.

####N-way Merging
Then, we merged all the blocks generated using n-way merging, where n is the total number of blocks. This is done by reading (MAX_LINES_IN_MEM / n) number of lines from each block, and adding each term and its posting into a priority queue. We then process all items in the priority queue in order, append all postings with the same term together, sort them and continue with the next queue item. 

If all the (MAX_LINES_IN_MEM / n) number of items from a specific block are fully processed, we load another set of items from that specific block into memory.

When the number of terms or lines in memory reaches MAX_LINES_IN_MEM, we write out the terms into out_dict and out_postings. Reset the memory and repeat the merging process until no more item in the queue. 

###About Searching


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0222182R, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
