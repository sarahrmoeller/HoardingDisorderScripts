"""
This file combs through the data and finds any documents that don't have any
punctuation in them.
"""
import os
from utils.raw import doc_paths


for doc_path in doc_paths:
    with open(doc_path, 'r') as f:
        content = f.read()
    if '.' not in content:
        print(os.path.basename(doc_path))