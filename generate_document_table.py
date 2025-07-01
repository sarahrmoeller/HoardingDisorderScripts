import pandas as pd
from tqdm import tqdm
import utils.datasaur as data 
import utils.ling as ling


if __name__ == "__main__":
    table_rows = []
    
    pbar = tqdm(data.by_project.items())
    for project, docs in pbar:
        pbar.set_description(project)
        # List of rows in the csv file 
        project_rows = list(map(lambda doc: { 
            'Project' : project,
            'Document Name' : doc.name, 
            'Hoarder Flag' : doc.hoarder_flag,
            **doc.label_counts,
            'TTR-Interviewer' : ling.type_token_ratio(doc.tokens("Interviewer",
                                                                 flat=True)), # type: ignore
            'TTR-Participant' : ling.type_token_ratio(doc.tokens("Participant",
                                                                 flat=True)), # type: ignore
            'TTR-sent-Interviewer' : ling.type_token_ratio(doc.tokens(
                                                                "Interviewer",
                                                                flat=True),
                                                           per_sent=True), # type: ignore
            'TTR-sent-Participant' : ling.type_token_ratio(doc.tokens(
                                                                 "Participant",
                                                                 flat=True),
                                                           per_sent=True), # type: ignore
            'ASL-Interviewer' : ling.average_sentence_length(
                doc.tokens("Participant")), # type: ignore
            'ASL-Participant' : ling.average_sentence_length(
                doc.tokens("Interviewer")), # type: ignore
            'NP-counts-Interviewer' : ling.get_np_counts(doc.tokens("Interviewer")),
            'NP-counts-Participant' : ling.get_np_counts(doc.tokens("Participant")),
            'NP-ratio-Interviewer' : ling.get_np_ratios(doc.tokens("Participant")),
            'NP-ratio-Participant' : ling.get_np_ratios(doc.tokens("Interviewer"))
        }, docs))
        table_rows.extend(project_rows)

    df = pd.DataFrame(table_rows)
    df.to_csv('./out/document_table.csv', index=False)