import pandas as pd
import utils.ling as ling
import utils.raw as raw
from utils.document import RawDocument


if __name__ == "__main__":
    csv_rows = []

    for doc_path in raw.doc_paths:
        doc = RawDocument(doc_path)
        stanza_doc = ling.nlp(doc.content("Participant"))
        speaker_tokens = [[token.text for token in sent.tokens] 
                          for sent in stanza_doc.sentences] # type: ignore

        csv_rows.append({
            'Document Name': doc.name,
            'TTR': ling.type_token_ratio(speaker_tokens),
            'ASL': ling.average_sentence_length(speaker_tokens),
            'NPR': ling.NP_ratio(stanza_doc) # type: ignore
        })

    df = pd.DataFrame(csv_rows)
    df.to_csv('./out/ling_table.csv', index=False)