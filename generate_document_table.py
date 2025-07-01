import pandas as pd
from tqdm import tqdm
import utils.datasaur as data 
import utils.ling as ling


if __name__ == "__main__":
    # List of rows in the csv file 
    table_rows = []
    
    pbar = tqdm(data.by_doc)
    for doc in pbar:
        pbar.set_description(f"{doc}")

        interviewer_tokens = doc.tokens("Interviewer", flat=True) # type: ignore
        participant_tokens = doc.tokens("Participant", flat=True) # type: ignore

        interviewer_nlp = ling.nlp(doc.content_by_speaker("Interviewer"))
        participant_nlp = ling.nlp(doc.content_by_speaker("Participant"))

        row = { 
            'Project' : doc.project,
            'Document Name' : doc.name, 
            'Hoarder Flag' : doc.hoarder_flag,
            **doc.label_counts,
            'TTR-Interviewer' : ling.type_token_ratio(interviewer_tokens),
            'TTR-Participant' : ling.type_token_ratio(participant_tokens),
            'TTR-sent-Interviewer' : ling.type_token_ratio(interviewer_tokens),
            'TTR-sent-Participant' : ling.type_token_ratio(participant_tokens),
            'ASL-Interviewer' : ling.average_sentence_length(
                doc.tokens("Participant")), # type: ignore
            'ASL-Participant' : ling.average_sentence_length(
                doc.tokens("Interviewer")), # type: ignore
            'NP-counts-Interviewer' : ling.get_np_counts(interviewer_nlp),
            'NP-counts-Participant' : ling.get_np_counts(participant_nlp),
            'NP-ratio-Interviewer' : ling.get_np_ratios(interviewer_nlp),
            'NP-ratio-Participant' : ling.get_np_ratios(participant_nlp)
        }
        table_rows.append(row)

    df = pd.DataFrame(table_rows)
    df.to_csv('./out/document_table.csv', index=False)