"""
In Transcript 012, each speaker label for the Interviewer is mislabeled as 
'Interviewee'. This script goes through each document in the datasaur data, 
inspects its JSON, and replaces each instance of 'Interviewee' with 
'Interviewer' in the row data.

This script is meant to be run from the project's root directory.
"""
from utils import datasaur as data
import json


for doc in data.by_transcript["012"]:
    # Modify doc.row_data and fix Interviewer label
    for i in range(len(doc.row_data)):
        # Fix labels in the lines
        doc.row_data[i]['content'] = doc.lines[i].replace("Interviewee:", 
                                                          "Interviewer:")
        # Fix labels in the tokens
        for j in range(len(doc.row_data[i]['tokens'])):
            token: str = doc.row_data[i]['tokens'][j]
            token = token.replace("Interviewee:", "Interviewer:") 
            doc.row_data[i]['tokens'][j] = token
    # Switch out old row data in the JSON dump with the new one
    doc.json_dump['rows'] = doc.row_data

    with open(data.review_dir(doc.project) + doc.name + '.json', "w") as f:
        json.dump(doc.json_dump, f)