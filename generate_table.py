import pandas as pd
from tqdm import tqdm
from utils.datasaur import data


if __name__ == "__main__":
    table_rows = []
    
    pbar = tqdm(data.items())
    for project, docs in pbar:
        pbar.set_description(project)
        # List of rows in the csv file 
        project_rows = list(map(lambda doc: { 
            'Project' : project,
            'Document Name' : doc.name, 
            'Hoarder Flag' : doc.hoarder_flag,
            **doc.label_counts,
            'TTR' : doc.type_token_ratio,
            'ASL' : doc.average_sentence_length,
        }, docs))
        table_rows.extend(project_rows)

    df = pd.DataFrame(table_rows)
    df.to_csv('./out/table.csv', index=False)