import pandas as pd
from tqdm import tqdm
import utils.datasaur as data 


if __name__ == "__main__":
    # List of rows in the csv file 
    table_rows = []
    
    pbar = tqdm(data.by_doc)
    for doc in pbar:
        pbar.set_description(f"{doc}")

        row = { 
            'Project' : doc.project,
            'Document Name' : doc.name, 
            'Hoarder Flag' : doc.hoarder_flag,
            **doc.label_counts,
        }
        table_rows.append(row)

    df = pd.DataFrame(table_rows)
    df.to_csv('./out/document_table.csv', index=False)