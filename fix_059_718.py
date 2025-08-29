"""
Fix this one specific line in this one specific document.
"""
import utils.datasaur as data
from utils.transcript import Transcript
import json


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

with open(data.review_dir(doc.project) + doc.name + '.json', "w") as f:
    json.dump(doc.json_dump, f)