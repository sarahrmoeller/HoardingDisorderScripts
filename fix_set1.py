"""
All documents from set 1 start with a 0, but we wanted them to start with a 1.
This is consistent, so all this script does is add a 1 to the beginning of 
every filename in set 1.
"""
# In the text files
from utils.data.raw import doc_paths
import os


for doc_path in doc_paths:
    doc_name = os.path.basename(doc_path)
    set_num = doc_name[0]
    if set_num == '0':
        new_name = '1' + doc_name
        new_path = doc_path.replace(doc_name, new_name)
        # Rename the file
        os.rename(doc_path, new_path)
        print(f'Renamed {doc_name} to {new_name}')

# # In datasaur
# import utils.datasaur as data


# for doc in data.by_doc:
#     if doc.set == '1':
#         old_name = doc.name
#         new_name = '1' + old_name
#         old_path = doc.path
#         new_path = old_path.replace(old_name, new_name)
#         # Rename the file
#         os.rename(old_path, new_path)
#         print(f'Renamed {old_name} to {new_name}')

