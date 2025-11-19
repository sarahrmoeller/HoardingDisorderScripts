"""
This file aggregates a bunch of changes, all summarized in `DATA_CLEANING.md `.
"""
from collections import Counter
import random
import utils.datasaur as data
from utils.transcript import Transcript
import json
import os


"""Speaker Label Corrections"""

"""
## Fix Transcript 012 speaker labels

In Transcript 012, the speaker label "Interviewee" was mistakenly labeled as
"Interviewer". This code corrects that error by replacing all instances of
"Interviewee" with "Interviewer".
"""
for doc in Transcript("012").docs:
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

    with open(doc.path, "w") as f:
        json.dump(doc.json_dump, f)

"""
## De-identify Documents

This script loops over every single document, checks whether it has someone's
name in the text that we know of, like "Rebecca" or "Christian", and replace it
something appropriate that de-identifies it.
"""
replacements = {
    **dict.fromkeys(["Rebecca", "Christian"], "Interviewer"), 
    **dict.fromkeys(["Ann", "Lauren Mellin", "Josha"], "NAME"), 
    **dict.fromkeys(["Sand", "Buttonheim"], "LOCATION"),
}

for doc in data.by_doc:
    # If both Rebecca and Christian are present, we can distinguish them
    # (not necessary, but makes reading the transcript easier)
    if {"Rebecca", "Christian"}.issubset(doc.speaker_set(restrict=False)):
        replacements["Rebecca"] = "Interviewer 1"
        replacements["Christian"] = "Interviewer 2"
    else:
        replacements["Rebecca"] = "Interviewer"
        replacements["Christian"] = "Interviewer"

    # Modify doc.row_data
    for i in range(len(doc.row_data)):
        # Fix labels in the lines
        for name, repl in replacements.items():
            doc.lines[i] = doc.lines[i].replace(name, repl)
        doc.row_data[i]['content'] = doc.lines[i]
        # Fix labels in the tokens
        for j in range(len(doc.row_data[i]['tokens'])):
            token: str = doc.row_data[i]['tokens'][j]
            for name, repl in replacements.items():
                token = token.replace(name, repl)
            doc.row_data[i]['tokens'][j] = token
    # Switch out old row data in the JSON dump with the new one
    doc.json_dump['rows'] = doc.row_data

    with open(doc.path, "w") as f:
        json.dump(doc.json_dump, f)

"""
## Fix Misspelled Speaker Labels

This code fixes speaker labels that we identified to be misspelled in some way.
"""
misspellings = {
    "Speaker" : ["Speake", "Spaker", "Speaker1", "1:Speaker", "Speakerr"],
    "Participant" : ["2Participant"],
    "Interviewer" : ["Interviewer1", "1:Interviewer"],
    "Note" : ["1:Note"] # extra thing we caught---we'll fix even though it isn't a speaker label
}
for doc in data.by_doc:
    # Modify doc.row_data and labels
    for i in range(len(doc.row_data)):
        # Fix labels in the lines
        for key in misspellings:
            for misspelled in misspellings[key]:
                doc.row_data[i]['content'] = (doc.row_data[i]['content']
                                                 .replace(misspelled, key))
        # Fix labels in the tokens
        for j in range(len(doc.row_data[i]['tokens'])):
            token: str = doc.row_data[i]['tokens'][j]
            for key in misspellings:
                if any(misspelling in token 
                       for misspelling in misspellings[key]):
                    # token = key (correct spelling)
                    fixed_token = (doc.row_data[i]['tokens'][j]
                                      .replace(token, key))
                    doc.row_data[i]['tokens'][j] = fixed_token
                    break # Found token's match, no need to keep checking
    # Switch out old row data in the JSON dump with the new one
    doc.json_dump['rows'] = doc.row_data

    with open(doc.path, "w") as f:
        json.dump(doc.json_dump, f)

"""
## Fix Specific Line in Document 3001_039.txt

Literally just change "Interviewer:Right" to "Interviewer: Right" in this 
document. Necessary for speaker label detection.
"""
doc = Transcript("3001")["039"]
bad_line_index = [i for i in range(len(doc.lines)) 
                  if "Interviewer:Right" in doc.lines[i]][0]
doc.row_data[bad_line_index]['content'] = (doc.lines[bad_line_index]
                                              .replace("Interviewer:Right", 
                                                       "Interviewer: Right"))
# Fix labels in the tokens
tokens: list[str] = doc.row_data[bad_line_index]['tokens']
# In this case, this line only had one token, so we can just delete it
# and replace it with two new ones
tokens[0] = "Interviewer:"
tokens.insert(1, "Right")

# Switch out old row data in the JSON dump with the new one
doc.json_dump['rows'] = doc.row_data
with open(doc.path, "w") as f:
    json.dump(doc.json_dump, f)


"""/Speaker Label Corrections"""


"""Remove duplicate documents"""
doc_names = [doc.name for doc in data.by_doc]
doc_name_cntr = Counter(doc_names)
duplicate_doc_names = [name for name, count in doc_name_cntr.items() 
                       if count >= 2]
                # list(set()) to remove possible duplicates in the list
dupdocs = {name : list(set((doc for doc in data.by_doc if doc.name == name)))
           for name in duplicate_doc_names}

for name, docs in dupdocs.items():
    # Choose random element of the pair to keep
    print(name, [doc.path for doc in docs])
    doc_to_keep = random.choice(docs)
    # Remove all other duplicates
    docs.remove(doc_to_keep)
    for doc in docs:
        os.remove(doc.path)
        print(f"Removed duplicate document {doc.path}")


"""
## Fix Transcripts 001-007

This script fixes transcripts 001 to 007, or more accurately fixes all 
documents that are said to be from that range---some of these documents are 
actually from transcripts 2001 to 2007.

After deidentification, we checked in `001-007_fixes.ipynb` that not a 
single document in any of the projects labeled HD_set1 have speakers that are 
labeled "Interviewee". Thus, assuming that all documents in HD_set1 are 
actually hoarding documents, this is sufficient evidence to conclude that if a
document has a speaker labeled "Interviewee", it is not a hoarding document, 
and is in fact from transcripts 2001 to 2007.
"""
transcript_numbers = ['001', '002', '003', '004', '005', '006', '007']

for tn in transcript_numbers:
    for doc in Transcript(tn).docs:
        unique_set2_speaker_labels = {'Interviewee', 'P1', 'P2', 'P3'}
        if any(speaker_label in doc.speaker_set() 
            for speaker_label in unique_set2_speaker_labels):
            old_path = doc.path
            new_name = '2' + doc.name
            new_path = (os.path.dirname(old_path) + '/' + 
                        new_name.rstrip('.txt') + '.json')
            with open(old_path, 'w') as f:
                print(f'Fixing {old_path}')
                doc.json_dump['data']['document']['name'] = new_name
                json.dump(doc.json_dump, f)
            os.rename(old_path, new_path)
            print(f'Renamed {old_path} to {new_path}')


"""Fix Transcript 2005"""
for doc in Transcript("2005").docs:
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

    with open(doc.path, "w") as f:
        json.dump(doc.json_dump, f)


"""
## Fix Transcript 2005 Speaker Labels

In Transcript 2005, the speaker labels "P3" and "Interviewee" are switched. 
This script finds all documents under transcript 2005 and switches them back.

Note that this code needs to be run after the previous code, as otherwise some 
of the documents from 2005 will not be targeted, as they will be mistakenly 
labeled under transcript 005.
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

    with open(doc.path, "w") as f:
        json.dump(doc.json_dump, f)


"""
## Fix Broken Timestamps

Go through a number of specific files in which we found timestamps that were
poorly formatted and fix their formatting. This correction is necessary so that
timestamps can be properly removed in cleaning.
"""
# Found through datasaur diving
broken_timestamps = [
    # With spaces
    ('07: 27', '07:27', 4, ['3001', '030']),
    ('07: 27', '07:27', 23, ['3001', '048']),
    ('26: 35', '26:35', 14, ['2004', '053']),
    ('03: 58', '03:58', 9, ['3001', '082']),
    ('07: 34', '07:34', 1, ['3001', '083']),
    ('30: 31', '30:31', 5, ['3001', '087']),
    ('35: 11', '35:11', 9, ['3001', '088']),
    ('09: 22', '09:22', 9, ['059', '716']),
    ('34: 54', '34:54', 34, ['3001', '007']),
    ('38: 23', '38:23', 19, ['3001', '008']),
    ('26: 48', '26:48', 26, ['3001', '005']),
    ('03: 44', '03:44', 27, ['3001', '000']),
    ('41: 50', '41:50', 29, ['3001', '009']),
    ('43: 27', '43:27', 41, ['3001', '009']),
    ('31: 23', '31:23', 30, ['3001', '006']),
    ('[26: 35]', '[26:35]', 14, ['2004', '053']),
    ('09: 22-', '09:22-', 9, ['059', '716']),
    # With letters
    ('34:4y', '34:46', 44, ['054', '671']),
    ('36:4o', '36:40', 15, ['3001', '034'])
]


for broken_ts, fixed_ts, line_num, [trans_num, doc_num] in broken_timestamps: 
    doc = Transcript(trans_num)[doc_num]

    # Fix line
    doc.lines[line_num] = doc.lines[line_num].replace(broken_ts, fixed_ts)
    doc.row_data[line_num]['content'] = doc.lines[line_num]

    # Fix tokens
    token_line: list[str] = doc.tokens[line_num]
    if ' ' in broken_ts:
        # Special fix for broken timestamps with spaces
        broken_ts_parts = broken_ts.split()
        if any(part not in token_line for part in broken_ts_parts):
            continue
        fixed_token_index = token_line.index(broken_ts_parts[0])
        token_line[fixed_token_index] = fixed_ts
        del token_line[fixed_token_index + 1]
    else:
        # Normal fix
        try:
            index = [i for i in range(len(token_line)) 
                    if broken_ts in token_line[i]][0]
        except IndexError:
            continue
        token_line[index] = token_line[index].replace(broken_ts, fixed_ts)
    doc.row_data[line_num]['tokens'] = token_line

    doc.json_dump['rows'] = doc.row_data

    with open(doc.path, "w") as f:
        json.dump(doc.json_dump, f)


"""
## Fix Specific Line in Document 059_718.txt

Document 059_718.txt contains this line
```
Interviewer19:09- Ok sounds good.
```
This script just changes this to
```
Interviewer 19:09- Ok sounds good.
```
Without doing this, the regex that finds timestamps will not be able to 
identify the timestamp with it being "attached" to word characters.
"""
doc = Transcript("059")["718"]
bad_line_index = [i for i in range(len(doc.lines)) 
                  if "Interviewer19:09-" in doc.lines[i]][0]
doc.row_data[bad_line_index]['content'] = doc.lines[bad_line_index].replace("Interviewer19:09-", 
                                                                            "Interviewer 19:09-")
# Fix labels in the tokens
tokens = doc.row_data[bad_line_index]['tokens']
tokens[0] = "Interviewer"
tokens.insert(1, "19:09-")
doc.row_data[bad_line_index]['tokens'] = tokens

# Switch out old row data in the JSON dump with the new one
doc.json_dump['rows'] = doc.row_data

with open(doc.path, "w") as f:
    json.dump(doc.json_dump, f)
