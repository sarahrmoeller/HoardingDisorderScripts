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
            'TTR' : ling.type_token_ratio(doc.full_content),
            'ASL' : ling.average_sentence_length(doc.full_content),
        }, docs))
        table_rows.extend(project_rows)

    df = pd.DataFrame(table_rows)
    df.to_csv('./out/document_table.csv', index=False)