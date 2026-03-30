import utils.data.raw as raw
from utils.document import TextDocument
from itertools import product
from pprint import pprint


raw_docs = [TextDocument(dp) for dp in raw.doc_paths]

pprint([doc_pair for doc_pair in product(raw_docs, repeat=2)
        if doc_pair[0].full_text == doc_pair[1].full_text and
           doc_pair[0].name != doc_pair[1].name])