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

            # Locate term in the dictionary
            doc_frq = self.dictionary[postings][0]
            pointer = self.dictionary[postings][1]

            # Retrieve postings list
            f = open(self.postings_file, 'r')
            f.seek(pointer, 0)
            p1_as_string = f.readline().strip()

            # Put the postings into a list 
            p1_doc_ids = p1_as_string.split()
            postings = p1_doc_ids[1:]
            postings = list(map(int, postings))

        return postings # return as tuple, including the doc_freq also (how many documents in this list)

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
       
    '''
    Takes in two lists of doc ids and returns a list of common docs.
    IMPLEMENT SKIP POINTERS HERE!!! 
    '''   
    def intersect(self, p1_doc_ids, p2_doc_ids):
        common_documents = []
        print(p1_doc_ids, p2_doc_ids)

        i = j = 0
        len1 = len(p1_doc_ids)
        len2 = len(p2_doc_ids)

        while (i < len1 and j < len2): 

          # Matched postings
          if p1_doc_ids[i] == p2_doc_ids[j]:
            common_documents.append(p1_doc_ids[i])
            i += 1
            j += 1

          elif int(p1_doc_ids[i]) < int(p2_doc_ids[i]):
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

        while i < len(p1_doc_ids) and j < len(p2_doc_ids):
            if p1_doc_ids[i] < p2_doc_ids[j]:
                common_documents.append(p1_doc_ids[i])
                i += 1

            elif p1_doc_ids[i] > p2_doc_ids[j]:
                common_documents.append(p2_doc_ids[j])
                j += 1

            elif p1_doc_ids[i] == p2_doc_ids[j]:
                i += 1
                j += 1
            
        common_documents.extend(p1_doc_ids[i:])
        common_documents.extend(p2_doc_ids[j:])
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
        print(postings, all_docs)

        while i < len(postings):

            # Only one conditional is needed as the doc ids in postings will always be a subset of all the docs. 
            if postings[i] > all_docs[j]:
                complement_documents.append(all_docs[j])
                j += 1

            # Discard this document
            if postings[i] == all_docs[j]:
                i += 1
                j += 1

        # Add the rest of the complemented documents
        complement_documents.extend(all_docs[j:])

        return complement_documents


