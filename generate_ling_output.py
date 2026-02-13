import pandas as pd
import utils.ling as ling
import utils.raw as raw
from utils.document import RawDocument


if __name__ == "__main__":
    csv_rows = []

    for doc_path in raw.doc_paths:
        doc = RawDocument(doc_path)
        csv_rows.append({
            'Document Name': raw.get_doc_path(doc_path).split('/')[-1],
            'TTR': ling.type_token_ratio(doc.lines("Participant")),
            'ASL': ling.average_sentence_length(doc.lines("Participant"))
        })