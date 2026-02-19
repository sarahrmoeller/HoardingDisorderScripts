"""
This file combs through the data and finds any documents that don't have any 
end-of-sentence characters in them. We're only looking for periods (.) since 
these are crucial for sentence segmentation, but we'll note if there are 
other end-of-sentence characters.
"""
from utils.data.raw import doc_paths
import csv
import os


EOS_CHARS = {'.', '!', '?'} # end-of-sentence characters


files_without_period = []
for doc_path in doc_paths:
    with open(doc_path, 'r') as f:
        content = f.read()
    if '.' not in content:
        files_without_period.append({
            'name': os.path.basename(doc_path),
            'has_exclamation': '!' in content,
            'has_question': '?' in content
        })


with open('files_without_period.txt', 'w') as out_file:
    writer = csv.DictWriter(out_file, 
                            fieldnames=['name', 'has_exclamation', 
                                        'has_question'])
    writer.writeheader()
    writer.writerows(files_without_period)