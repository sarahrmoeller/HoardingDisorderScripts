# Scripts for Running Statistics on Hoarding Disorder Data

Here reside the scripts for running Statistics on the data we have on Hoarding Disorder patients and control, 
including labeled data from datasaur and the original unlabeled data (TBD). 

## How to Replicate our Python Environment

These python scripts were run in a a python virtual environment with `venv`. To replicate our results, we recommend the following:
1. Clone our repository.
2. Check for `python` version 3.10.19 and `pip` version 26.0.1, then create a new virtual environment with these versions. We created our environment with `{path/to/python3} -m venv .venv`.
4. Run `source .venv/bin/{your activation script}` from the project's root directory to activate the virtual environment.
5. Run `pip install -r requirements.txt` to install all needed dependencies to replicate our work. 

We tested this on multiple computers with the given versions.  
It may be possible to get our code working using `conda`/`anaconda`, but we have not tested this. 
We are working to port our environment to nix.

## Project Structure

### Data

All data that is used for this project can be found in the `./data` folder. 
See `./data/mathews/documents/README.md` for a full explanation of the data.

### Code

If you are working directly on this project, you will likely find that most—if not all—of what you will need to work with this project is in the `./utils/` directory.
This contains a number of functions and classes written in python useful for analyzing individual transcripts and documents, as well as making queries on a large number of documents.


## How to Use Our Code to Inspect the Datasaur Data

The meat of this project is the `Document` class within `./utils/document.py`. 
Given a path to a .json file from the datasaur data, this class
extracts and deduces important information about each document, including label data. 
Some examples:

- `Document.name`: Document's name, i.e. `'001_001.txt'`
- `Document.project`: Document's project, i.e. `'HD_set1_1-7'`
- `Document.hoarder_flag`: 1 if the document is a hoarding document, 0 otherwise (determined by the document's name)
- `Document.lines`: A list of each line (separate by newlines) in the document.  
- `Document.full_content`: The document's entire text content in one string
- `Document.content_by_speaker(speaker: str)`: The set of all text spoken by a particular speaker, Interviewer or Participant, in a document.
  Pass in either "Interviewer" or "Participant" to get the text from the speaker you are looking for.
- `Document.speaker_set(restrict=True)`: The set of all speaker labels (strings followed by a colon, i.e. "Interviewer: ") found in the document.
   - The `restrict` option, set to `True` by default, filters the speaker labels to only show strings that we know are valid speaker labels.
     For instance, if the labels "Interviewer:" and "Spongebob:" are found and `restrict=True`, only the former would be returned.
- `Document._labels`: A list of the document's labels, organized as tuples (Label, Speaker).
  Each tuple tells us which label is found (i.e. Incomplete Thought, Clarification) and which speaker the label came from (Interviewer or Participant).
- `Document.label_counts`: A dictionary containing all relevant information regarding label counts.
  The dictionary is organized in the format "[Label]-[Type]". For instance:
     - The entry "Incomplete Thought-Participant" is the number of Incomplete Thought labels found in the Participant's speech in this document. There
       will also be an entry with Interviewer in the place of Participant, which is interpreted the same way.
     - The entry "Clarification-Total" is the total number of clarification labels in general, spoken either by Interviewer or Participant.
     - The entry "Total" is the total number of labels in the document, regardless of type or speaker.  
- `Document.tokens(speaker: str)`: A list of all tokens spoken by a particular speaker.

Though many of these functions are designed to provide information on both Interivewer and Participant speech, you will likely only be concerned with Participant speech.
If so, please focus soley on Participant speech by passing in the string "Participant" to functions that differentiate between speakers, or by ignoring entries
in lists or dictionaries that involve Interviewers.

Further, `utils/datasaur.py` contains a few data structures that organize all of the document objects:

```python
# Run this in the project root
import utils.datasaur as data

data.by_project # dict[project name -> list of docs in that project]
data.by_doc # list of all documents
data.by_transcript # dict[transcript name (i.e. '002') -> list of all docs corresponding to that transcript (i.e. '002_015.txt')]
```

You can use these structures to make queries about the data, often with some form of Pythonic comprehension. For instance, the following code finds the set of all speaker labels for all Hoarding documents found in the HD_set1 projects:

```python
>>> hdsets = {proj: docs for proj, docs in data.by_project.items() if proj.startswith('HD_set1')}
>>> hdset_docs = [doc for doclist in hdsets.values() for doc in doclist] # flattened list
>>> hdset_speakers = {speaker for doc in hdset_docs for speaker in doc.speaker_set}
>>> hdset_speakers
{'Interviewee', 'Interviewer', 'Participant'}
```