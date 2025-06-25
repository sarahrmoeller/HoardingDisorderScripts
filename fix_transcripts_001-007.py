"""
This script fixes transcripts 001 to 007, or more accurately fixes all 
documents that are said to be from that range---some of these documents are 
actually from transcripts 2001 to 2007.

After running deidentify.py, we checked in 001-007_fixes.ipynb that not a 
single document in any of the projects labeled HD_set1 have speakers that are 
labeled "Interviewee". Thus, assuming that all documents in HD_set1 are 
actually hoarding documents, this is sufficient evidence to conclude that if a
document has a speaker labeled "Interviewee", it is not a hoarding document, 
and is in fact from transcripts 2001 to 2007.

As usual, run this script from the project's root.
"""
import os
import utils.datasaur as data
import json


transcripts = ['001', '002', '003', '004', '005', '006', '007']
target_docs = (doc for doc in data.by_doc
               if doc.transcript_number in transcripts)

for doc in target_docs:
    unique_set2_speaker_labels = {'Interviewee', 'P1', 'P2', 'P3'}
    if any(speaker_label in doc.speaker_set() 
           for speaker_label in unique_set2_speaker_labels):
        project_path = data.review_dir(doc.project)
        new_name = '2' + doc.name
        old_path = project_path + doc.name + '.json'
        with open(old_path, 'w') as f:
            print(f'Fixing {old_path}')
            doc.json_dump['data']['document']['name'] = new_name
            json.dump(doc.json_dump, f)
        new_path = project_path + new_name + '.json'
        os.rename(old_path, new_path)
        print(f'Renamed {old_path} to {new_path}')
                  