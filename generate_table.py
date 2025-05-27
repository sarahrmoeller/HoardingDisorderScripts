import os
import pandas as pd
from utils.docment import Document

if __name__ == "__main__":
    table_rows = []
    project_dirs = os.listdir('./data')
    project_dirs.remove('.gitignore')

    for project_dir in project_dirs:
        # Only looking in the REVIEW directory, as this directory contains all
        # adjudicated documents (and not documents with labels from only one 
        # person)
        review_dir = f"./data/{project_dir}/REVIEW/"
        json_files = os.listdir(review_dir)

        project_docs = [Document(review_dir + file) for file in json_files]
        # List of rows in the csv file 
        project_rows = list(map(lambda doc: { 
            'Project' : project_dir,
            'Document Name' : doc.name, 
            'Hoarder Flag' : doc.hoarder_flag,
            **doc.label_counts,
            'TTR' : doc.type_token_ratio,
            'ASL' : doc.average_sentence_length,
        }, project_docs))
        table_rows.extend(project_rows)

    df = pd.DataFrame(table_rows)
    df.to_csv('./out/table.csv', index=False)