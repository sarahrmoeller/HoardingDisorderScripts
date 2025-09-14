"""
Fixing speaker labels that we identified to be misspelled in some way.
"""
from utils import datasaur as data
import json


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
                doc.row_data[i]['content'] = doc.row_data[i]['content'] \
                                                .replace(misspelled, key)
        # Fix labels in the tokens
        for j in range(len(doc.row_data[i]['tokens'])):
            token: str = doc.row_data[i]['tokens'][j]
            for key in misspellings:
                if token in misspellings[key]:
                    # token = key (correct spelling)
                    doc.row_data[i]['tokens'][j] = key
                    break # Found token's match, no need to keep checking
    # Switch out old row data in the JSON dump with the new one
    doc.json_dump['rows'] = doc.row_data

    with open(data.review_dir(doc.project) + doc.name + '.json', "w") as f:
        json.dump(doc.json_dump, f)