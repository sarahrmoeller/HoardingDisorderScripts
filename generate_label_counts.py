from collections import Counter
import json
import os
import pandas as pd

rows = []
project_dirs = os.listdir('./data')
project_dirs.remove('.gitignore')
# List of all labels in the projects
LABELS = {
    'Incomplete Thought',
    'Self Correction',
    'Clarification',
    'Generic Disfluency',
    'Misspeak',
    'Unclear',
    'Overlap'
}
for project_dir in project_dirs:
    # Only looking in the REVIEW directory since this should contain all documents
    # with labels that have been agreed upon
    review_dir = f"./data/{project_dir}/REVIEW/"

    # Get all .json files in REVIEW dir
    json_files = [
        f for f in os.listdir(review_dir) if os.path.splitext(f)[1] == '.json'
    ]

    project_rows = [dict()] * len(json_files) # List of rows in the csv file 
    # This loop populates the rows list---we loop over an index so that we 
    # don't need to create a new list isn't created in memory after every 
    # .append method
    for i in range(len(json_files)):
        file = json_files[i]
        hoarder_flag = int(file[0] == '0')

        with open(review_dir + file) as f:
            raw_data = json.load(f)
        data = raw_data['data']

        # This is where the meat is at
        doc_label_data = data['spanLabels']
        cntDict = Counter(
            [label['labelItem']['labelName'] for label in doc_label_data]
        )
        for label in set(LABELS).difference(cntDict.keys()):
            cntDict[label] = 0
        cntDict['Total'] = sum(cntDict.values())

        row = {
            'Project' : project_dir,
            'Document Name' : data['document']['name'], 
            'Hoarder Flag' : hoarder_flag,
            **cntDict
        }
        project_rows[i] = row
    rows.extend(project_rows)

df = pd.DataFrame(rows)
df.to_csv('./out/label_counts.csv', index=False)
