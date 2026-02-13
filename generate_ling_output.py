import pandas as pd
import utils.ling as ling
import utils.raw as raw
from utils.document import RawDocument
from tqdm import tqdm
import warnings


if __name__ == "__main__":
    csv_rows = []

    for doc_path in tqdm(raw.doc_paths):
        doc = RawDocument(doc_path)
        stanza_doc_part = ling.nlp(doc.content("Participant"))
        participant_tokens = [[token.text for token in sent.tokens] 
                          for sent in stanza_doc_part.sentences] # type: ignore
        if not participant_tokens:
            if doc.content("Interviewer"):
                warnings.warn(f"No participant content found in {doc.name}" +
                               "(Note: Interviewer content present)")
            else:
                raise ValueError(f"No content found in {doc.name} "
                                  "for any speaker")

        csv_rows.append({
            'Document Name': doc.name,
            'TTR': ling.type_token_ratio(participant_tokens),
            'ASL': ling.average_sentence_length(participant_tokens),
            'NPR': ling.NP_ratio_in_sd(stanza_doc_part)
        })

    df = pd.DataFrame(csv_rows)
    df.to_csv('./out/ling_table.csv', index=False)