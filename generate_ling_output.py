import pandas as pd
import utils.ling as ling
import utils.raw as raw
import utils.stanza as stnz
from utils.document import RawDocument


if __name__ == "__main__":
    csv_rows = []

    for doc_path in raw.doc_paths:
        doc = RawDocument(doc_path)
        stanza_doc = ling.nlp(doc.content("Participant"))

        csv_rows.append({
            'Document Name': raw.get_doc_path(doc_path).split('/')[-1],
            'TTR': ling.type_token_ratio(),
            'ASL': ling.average_sentence_length()
        })