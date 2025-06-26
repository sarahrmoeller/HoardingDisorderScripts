"""
In transcript 2005 (named this after running `fix_transcripts_001-007.py`), 
the speaker labels "P3" and "Interviewee" are switched. This script switches
them back.
"""
import utils.datasaur as data
import json


for doc in data.by_transcript['2005']:
    # Fix rows/lines
    for i in range(len(doc.lines)):
        line = doc.lines[i]
        if 'P3' in line:
            line = line.replace('P3', 'Interviewee')
        elif 'Interviewee' in line:
            line = line.replace('Interviewee', 'P3')
        doc.row_data[i]['content'] = line
        # Fix tokens
        for j in range(len(doc.tokens)):
            token = doc.tokens[j]
            if 'P3' in token:
                token = token.replace('P3', 'Interviewee')
            elif 'Interviewee' in token:
                token = token.replace('Interviewee', 'P3')
            doc.tokens[j] = token
        doc.row_data[i]['tokens'] = doc.tokens
    doc.json_dump['rows'] = doc.row_data

    with open(data.review_dir(doc.project) + doc.name + '.json', "w") as f:
        json.dump(doc.json_dump, f)