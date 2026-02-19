"""
This script loops over every single document, checks whether it has someone's
name in the text that we know of, like "Rebecca" or "Christian", and replace it
something appropriate that de-identifies it.
"""
import utils.data.datasaur as datasaur
import json


replacements = {
    **dict.fromkeys(["Rebecca", "Christian"], "Interviewer"), 
    **dict.fromkeys(["Ann", "Lauren Mellin", "Josha"], "NAME"), 
    **dict.fromkeys(["Sand", "Buttonheim"], "LOCATION"),
}


for doc in datasaur.docs:
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

    with open(datasaur.review_dir(doc.project) + doc.name + '.json', "w") as f:
        json.dump(doc.json_dump, f)