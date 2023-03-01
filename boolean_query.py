'''
Parent class for the 3 boolean queries. 
'''
class BooleanQuery:
    def __init__(self, dictionary, postings_file):
        self.dictionary = dictionary
        self.postings_file = postings_file

    '''
    Returns a list of docIDs as integers 
    '''
    def term_to_doc_ids(self, postings):
        # If postings is a term, retrieve postings list
        if (not isinstance(postings, list)):    
            
            # Locate term in the dictionary --> WHAT IF IT'S NOT INSIDE? NEED TO CATCH RIGHT? 
            doc_frq = self.dictionary[postings][0]
            pointer = self.dictionary[postings][1]

            # Retrieve postings list
            f = open(self.postings_file, 'r')
            f.seek(pointer, 0)
            postings_as_string = f.readline().strip()

            # Put the postings into a list 
            doc_ids = postings_as_string.split()
            postings = doc_ids[1:]

        # Return as a list of strings
        return postings

'''
Inherits from the BooleanQuery class.
'''
class AndQuery(BooleanQuery):

    '''
    Calls the intersect method
    '''    
    def eval(self, postings1, postings2):
        print('Parsing AND query...')


        # The variables postings1 and postings2 could be terms or a list of numbers
        postings1 = self.term_to_doc_ids(postings1)
        postings2 = self.term_to_doc_ids(postings2)

        common_documents = self.intersect(postings1, postings2)
        return common_documents
       
    def get_doc_id(self, doc_id_with_skip):
        doc_id = ""
        doc_skip = 0

        if "|" in doc_id_with_skip: 
            parts = doc_id_with_skip.split("|")
            doc_id = parts[0]
            doc_skip = int(parts[1])
        
        else: 
            doc_id = doc_id_with_skip

        return (int(doc_id), doc_skip)

    '''
    Takes in two lists of doc ids and returns a list of common docs.
    IMPLEMENT SKIP POINTERS HERE!!! 
    '''   
    def intersect(self, p1_doc_ids, p2_doc_ids):
        common_documents = []
        print("Intersecting these two: ", p1_doc_ids)
        print("Intersecting these two: ", p2_doc_ids)
        i = j = 0
        len1 = len(p1_doc_ids)
        len2 = len(p2_doc_ids)

        doc1_id = None
        doc2_id = None
        doc1_skip = 0
        doc2_skip = 0
        # p1_doc_ids has the structure [12002| 12806 13949 342 518 941| 1312] as STRINGS

        while (i < len1 and j < len2): 

            # Check for skip pointer
            if "|" in p1_doc_ids[i]: 
                parts = p1_doc_ids[i].split("|")
                doc1_id = parts[0]
                doc1_skip = int(parts[1])
            else:
                doc1_id = p1_doc_ids[i]
                doc1_skip = 0

            if "|" in p2_doc_ids[j]: 
                parts = p2_doc_ids[j].split("|")
                doc2_id = parts[0]
                doc2_skip = int(parts[1])
            else:
                doc2_id = p2_doc_ids[j]
                doc2_skip = 0

            print(doc1_id, doc1_skip)

            # Matched postings
            if int(doc1_id) == int(doc2_id):
                common_documents.append(doc1_id)
                i += 1
                j += 1

            elif int(doc1_id) < int(doc2_id):
                # If there is a skip, and the skipped to element is smaller than doc2, take it 
                # if doc1_skip != 0 and self.get_doc_id(p1_doc_ids[i + doc1_skip])[0] <= int(doc2_id):
                #     while (p1_doc_ids[i + doc1_skip])

                    # If new element is < p2_doc_ids[j] --> repeat loop

                    # If new element == p2_doc_ids[j] --> add 

                    # Else, don't take skip pointer

                # ----
                # curr_doc = p1_doc_ids[i]
                # while curr_doc has a skip pointer
                    # Take it, check if < p2_doc_ids[j], update curr_doc

                    # If == , add to common_docs
                    #add both

                    # If >, 

                i += 1

            else:
                j += 1

        return common_documents  


'''
Inherits from the BooleanQuery class.
'''
class OrQuery(BooleanQuery):

    ''' 
    Calls the merge method
    '''
    def eval(self, postings1, postings2):
        print('Parsing OR query...')

        # The variables postings1 and postings2 could be terms or a list of numbers
        postings1 = self.term_to_doc_ids(postings1)
        postings2 = self.term_to_doc_ids(postings2)

        common_documents = self.merge(postings1, postings2)
        return common_documents

    '''
    Merge the two postings, the result is a list of documents in ascending order e.g. ['1', '3', '5']
    '''
    def merge(self, p1_doc_ids, p2_doc_ids): 
        common_documents =[]
        i = 0
        j = 0

        doc1_id = None
        doc2_id = None

        print("Merging these two: ", p1_doc_ids, p2_doc_ids)

        while i < len(p1_doc_ids) and j < len(p2_doc_ids):

            # Strip the doc_id string
            if "|" in p1_doc_ids[i]: 
                parts = p1_doc_ids[i].split("|")
                doc1_id = parts[0]

            if "|" in p2_doc_ids[j]: 
                parts = p2_doc_ids[j].split("|")
                doc2_id = parts[0]

            # Merge
            if int(doc1_id) < int(doc2_id):
                common_documents.append(doc1_id)
                i += 1

            elif int(doc1_id) > int(doc2_id):
                common_documents.append(p2_doc_ids[j])
                j += 1

            elif int(doc1_id) == int(doc2_id):
                i += 1
                j += 1
            
        common_documents.extend(id.strip("|") for id in p1_doc_ids[i:])
        common_documents.extend(id.strip("|") for id in p2_doc_ids[j:])
        return common_documents

        # NOTE: THIS IS NOT SORTED
        # return list(set(p1_doc_ids + p2_doc_ids))

'''
Inherits from the BooleanQuery class.
'''
class NotQuery(BooleanQuery):

    ''' 
    Calls the get_complement method
    '''
    def eval(self, postings):
        print('Parsing NOT query...')

        # The variables postings could be a term or list of numbers
        postings = self.term_to_doc_ids(postings)
        
        # Get all doc ids
        f = open("all_doc_ids.txt", 'r')
        all_docs_in_string = f.readline().strip()

        # Put the docs into a list 
        all_docs = all_docs_in_string.split()
        all_docs = list(map(int, all_docs))

        complemented_documents = self.get_complement(postings, all_docs)
        return complemented_documents


    ''' 
    Merge the two postings, the result is a list of documents in ascending order e.g. ['1', '3', '5']
    '''
    def get_complement(self, postings, all_docs): 
        complement_documents = []
        i = 0
        j = 0
        doc_id = ""
        # print("Complementing this ", postings)

        while i < len(postings):

            if "|" in postings[i]: 
                parts = postings[i].split("|")
                doc_id = parts[0]
            else: 
                doc_id = postings[i]

            # Only one conditional is needed as the doc ids in postings will always be a subset of all the docs. 
            if int(doc_id) > all_docs[j]:
                complement_documents.append(str(all_docs[j]))
                j += 1

            # Discard this document
            if postings[i] == all_docs[j]:
                i += 1
                j += 1

        # Add the rest of the complemented documents
        complement_documents.extend(list(map(str, all_docs[j:])))

        return complement_documents


