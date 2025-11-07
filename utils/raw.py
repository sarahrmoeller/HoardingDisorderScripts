"""Utilities for accessing raw document files."""
import os


text_files_dir = './data/mathews/documents/text_files'


doc_paths = [root + '/' + file
             for root, dirs, files in os.walk(f'{text_files_dir}/raw/')
             for file in files if file.endswith('.txt')]
doc_names = [os.path.basename(path) for path in doc_paths]
transcript_numbers = set(map(
    lambda doc_name: doc_name.split('_')[0], doc_names
))
docs_by_transcript = {tn: [dp for dp in doc_paths
                           if os.path.basename(dp).startswith(tn)]
                      for tn in transcript_numbers}


def get_doc_path(doc_name: str) -> str:
    set_num = '1' if doc_name[0] == '0' else doc_name[0]
    return f'{text_files_dir}/raw/set0{set_num}/{doc_name}'