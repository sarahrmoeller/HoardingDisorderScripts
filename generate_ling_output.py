import pandas as pd
import utils.ling as ling
import utils.raw as raw


if __name__ == "__main__":
    csv_rows = []

    for doc_path in raw.doc_paths:
        with open(doc_path, 'r') as f:
            lines = f.readlines()
        csv_rows.append({
            'Document Name': raw.get_doc_path(doc_path).split('/')[-1],
            'TTR': ling.type_token_ratio(lines),
            'ASL': ling.average_sentence_length(lines)
        })