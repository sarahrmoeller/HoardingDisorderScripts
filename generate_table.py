from collections import Counter
import json
import os
import pandas as pd
from itertools import product

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
INTERVIEWER_NAMES = ["Interviewer", "Rebecca"]
PARTICIPANT_NAMES = ["Participant", "Interviewee"]
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
    # don't need to create a new list in memory after every 
    # .append method
    for i in range(len(json_files)):
        file = json_files[i]
        hoarder_flag = int(file[0] == '0')

        with open(review_dir + file) as f:
            raw_data = json.load(f)
        data = raw_data['data']

        # Get speakers for each row in the transcript

        # Each index in this list corresponds to a row in the document, and this
        # list tells you that row's speaker
        row_speakers = [''] * len(data['rows'])
        speaker = ""
        for j in range(len(data['rows'])):
            row = data['rows'][j]
            for column in row:
                if (column['content'].find(":") != -1):
                    slice_with_potential_speaker: str = column['content'].split(":")[0].title()
                    speaker_found = False
                    for name in INTERVIEWER_NAMES:
                        if name in slice_with_potential_speaker:
                            speaker = INTERVIEWER_NAMES[0]
                            break
                    # Don't look for participant name if we already found the interviewer
                    if not speaker_found: 
                        for name in PARTICIPANT_NAMES:
                            if name in slice_with_potential_speaker:
                                speaker = PARTICIPANT_NAMES[0]
                                break
                row_speakers[j] = speaker

        # Get row number of the label
        labels_in_doc = data['spanLabels']

        labels_with_speakers = [('', '')] * len(labels_in_doc)
        for k in range(len(labels_in_doc)):
            label = labels_in_doc[k]

            label_name = label['labelItem']['labelName']
            row_index = label['textPosition']['start']['row']
            speaker = row_speakers[row_index] 
            labels_with_speakers[k] = (label_name, speaker)

        cntDict = Counter(labels_with_speakers)
        for label, speaker in set(
            product(LABELS, ['Interviewer', 'Participant'])
        ).difference(cntDict.keys()):
            cntDict[label] = 0
        cntDict['Total'] = sum(cntDict.values())

        display_dict = {}
        for label in LABELS:
            display_dict[label+'–Interviewer'] = cntDict[(label, 'Interviewer')]
            display_dict[label+'–Participant'] = cntDict[(label, 'Participant')]
            display_dict[label+'–Total'] = cntDict[(label, 'Interviewer')] + cntDict[(label, 'Participant')]
        display_dict['Total'] = sum(cntDict.values())
        display_dict

        row = {
            'Project' : project_dir,
            'Document Name' : data['document']['name'], 
            'Hoarder Flag' : hoarder_flag,
            **display_dict
        }
        project_rows[i] = row
    rows.extend(project_rows)

df = pd.DataFrame(rows)
df.to_csv('./out/table.csv', index=False)
