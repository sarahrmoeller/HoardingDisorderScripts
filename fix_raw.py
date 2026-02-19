"""
This script combines all of the fixes listed in DATA_CLEANING.md for the raw
document data, applying them all in order.
"""
import os
from collections import Counter
from utils.data.raw import *


"""Step 0a: Remove non-txt files from raw data directories"""
for root, dirs, files in os.walk(f'{text_files_dir}/raw/'):
    for filename in files:
        if not filename.endswith('.txt'):
            os.remove(os.path.join(root, filename))

"""Step 0b. Fix Document 2001-003.txt: replace - with _"""
if '2001-003.txt' in os.listdir(f'{text_files_dir}/raw/set02'):
    os.rename(f'{text_files_dir}/raw/set02/2001-003.txt', 
              f'{text_files_dir}/raw/set02/2001_003.txt')


"""Fix transcript 012"""
for doc_path in docs_by_transcript['012']:
    with open(doc_path, 'r+') as f:
        content = f.read()
        f.seek(0)
        f.write(content.replace('Interviewee:', 'Interviewer:'))
        f.truncate()

"""Fix misspelled speaker labels and deidentify all documents"""
replacements = {
    **dict.fromkeys(["Rebecca", "Christian"], "Interviewer"), 
    **dict.fromkeys(["Ann", "Lauren Mellin", "Josha"], "NAME"), 
    **dict.fromkeys(["Sand", "Buttonheim"], "LOCATION"),
}
misspellings = {
    "Speaker" : ["Speake", "Spaker", "Speaker1", "1:Speaker", "Speakerr"],
    "Participant" : ["2Participant"],
    "Interviewer" : ["Interviewer1", "1:Interviewer"],
    "Note" : ["1:Note"] # extra thing we caught---we'll fix even though it isn't a speaker label
}

for dp in doc_paths:
    with open(dp, 'r+') as f:
        content = f.read()
        if "Rebecca" in content and "Christian" in content:
            replacements["Rebecca"] = "Interviewer 1"
            replacements["Christian"] = "Interviewer 2"
        for old, new in replacements.items():
            content = content.replace(old, new)
        for key in misspellings:
            for misspelling in misspellings[key]:
                content = content.replace(misspelling, key)
        f.seek(0)
        f.write(content)
        f.truncate()

"""Fix Document 3001_039.txt"""
with open(get_doc_path('3001_039.txt'), 'r+') as f:
    content = f.read()
    f.seek(0)
    f.write(content.replace('Interviewer:Right', 'Interviewer: Right'))
    f.truncate()

        
"""Fix filenames for all documents from transcripts 001-007"""
docs_to_check = [
    doc 
    for tn in ['001', '002', '003', '005', '006', '007']
    for doc in docs_by_transcript[tn]
]
unique_set2_speaker_labels = {'Interviewee', 'P1', 'P2', 'P3'}
for doc_path in docs_to_check:
    with open(doc_path, 'r') as f:
        content = f.read()
    if any(speaker_label in content 
           for speaker_label in unique_set2_speaker_labels):
        dir_path, filename = os.path.split(doc_path)
        new_name = '2' + filename
        new_path = dir_path + '/' + new_name
        os.rename(doc_path, new_path)
        print(f'Renamed {doc_path} to {new_path}')


"""Remove duplicates"""
doc_name_cntr = Counter(doc_names)
duplicate_doc_names = {name : count for name, count in doc_name_cntr.items()
                       if count >= 2}
# !! Not moving forward with this, as manual inspection showed that the
#    `duplicate_doc_names` dictionary was empty.

"""Fix transcript 2005"""
for doc_path in docs_by_transcript['2005']:
    with open(doc_path, 'r+') as f:
        content = f.read()
        content = content.replace('P3:', 'Temp:')
        content = content.replace('Interviewer:', 'P3:')
        content = content.replace('Temp:', 'P3:')
        f.seek(0)
        f.write(content)
        f.truncate()

"""Fix Document 059_718.txt"""
with open(get_doc_path('059_718.txt'), 'r+') as f:
    content = f.read()
    f.seek(0)
    f.write(content.replace('Interviewer19:09-', 'Interviewer 19:09 -'))
    f.truncate()

"""Fix timestamps in various documents"""
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
    doc_path = get_doc_path(f'{trans_num}_{doc_num}.txt')
    with open(doc_path, 'r+') as f:
        content = f.read()
        # Fix line
        content = content.replace(broken_ts, fixed_ts)
        f.seek(0)
        f.write(content)
        f.truncate()
