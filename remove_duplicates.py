from collections import Counter
import utils.datasaur as data
from itertools import product
import random
import os


doc_names = [doc.name for doc in data.by_doc]
doc_name_cntr = Counter(doc_names)
duplicate_doc_names = {name : count for name, count in doc_name_cntr.items()
                       if count >= 2}
duplicate_docs = [doc for doc in data.by_doc 
                  if doc.name in duplicate_doc_names]
dupdoc_pairs = [(doc1, doc2) for doc1, doc2 in product(duplicate_docs, 
                                                       repeat=2)
                if doc1.name == doc2.name and doc1 is not doc2]


if __name__ == "__main__":
    for pair in dupdoc_pairs:
        # Choose random element of the pair to delete
        doc_to_delete = random.choice(pair)
        os.remove(doc_to_delete.path)
        print("Removed", doc_to_delete)