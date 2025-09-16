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

        sdoc_int = doc.stanza_doc("Interviewer")
        sdoc_part = doc.stanza_doc("Participant")

        row = { 
            'Project' : doc.project,
            'Document Name' : doc.name, 
            'Hoarder Flag' : doc.hoarder_flag,
            **doc.label_counts,
            'TTR-Interviewer' : ling.type_token_ratio(doc.tokens_by_speaker("Interviewer", 
                                                                            per_sent=False), 
                                                      per_sent=False),
            'TTR-Participant' : ling.type_token_ratio(doc.tokens_by_speaker("Participant", 
                                                                            per_sent=False), 
                                                      per_sent=False),
            'TTR-Sent-Interviewer' : ling.type_token_ratio(doc.tokens_by_speaker("Interviewer")),
            'TTR-Sent-Participant' : ling.type_token_ratio(doc.tokens_by_speaker("Participant")),
            'ASL-Interviewer' : ling.average_sentence_length(
                doc.tokens_by_speaker("Interviewer")), # type: ignore
            'ASL-Participant' : ling.average_sentence_length(
                doc.tokens_by_speaker("Participant")), # type: ignore
            'NP-counts-Interviewer' : ling.count_nps_in_sd(sdoc_int),
            'NP-counts-Participant' : ling.count_nps_in_sd(sdoc_part), 
            'NP-ratio-Interviewer'  : ling.NP_ratio_in_sd(sdoc_int),
            'NP-ratio-Participant'  : ling.NP_ratio_in_sd(sdoc_part),
        }
        table_rows.append(row)

    df = pd.DataFrame(table_rows)
    df.to_csv('./out/document_table.csv', index=False)