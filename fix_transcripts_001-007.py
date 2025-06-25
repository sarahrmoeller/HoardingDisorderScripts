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


transcripts = ['001', '002', '003', '004', '005', '006', '007']
target_docs = (doc for doc in data.by_doc
               if doc.transcript_number in transcripts)

for doc in target_docs:
    if 'Interviewee' in doc.speaker_set():
        project_path = data.review_dir(doc.project)
        os.rename(project_path + doc.name + '.json', 
                  project_path + '2' + doc.name + '.json')