class AndQuery:

    def __init__(self, dictionary, postings_file) :
        self.dictionary = dictionary
        self.postings_file = postings_file
    
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
        
        return postings # return tuple of doc_freq also
        
    def eval(self, postings1, postings2):
        print('Parsing AND query...')

        '''
        The variables postings1 and postings2 could be terms or a list of numbers
        '''
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
              

class OrQuery:

    def __init__(self, dictionary, postings_file) :
        self.dictionary = dictionary
        self.postings_file = postings_file

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
        
        return postings # return tuple of doc_freq also

    def eval(self, postings1, postings2):
        print('Parsing OR query...')

        '''
        The variables postings1 and postings2 could be terms or a list of numbers
        '''
        postings1 = self.term_to_doc_ids(postings1)
        postings2 = self.term_to_doc_ids(postings2)

        common_documents = self.merge(postings1, postings2)
        print (common_documents)
        return common_documents

    '''
    Merge the two postings. 
    '''
    def merge(self, p1_doc_ids, p2_doc_ids): 
        common_documents =[]

        # NOTE: THIS IS NOT SORTED
        return list(set(p1_doc_ids + p2_doc_ids))
           