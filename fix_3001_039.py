"""
Literally just change "Interviewer:Right" to "Interviewer: Right".
"""

import utils.datasaur as data
from utils.transcript import Transcript
import json


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
with open(data.review_dir(doc.project) + doc.name + '.json', "w") as f:
    json.dump(doc.json_dump, f)