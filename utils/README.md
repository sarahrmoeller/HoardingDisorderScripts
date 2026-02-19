# How to Use the `utils` Module to Inspect The Data

Run all of the following examples **from the root directory**.

## Queries on Label Data

### Documents

For nearly anything you need to know about document data, look at the `docs` list within `utils.data.datasaur`.
This is a list of each datasaur document, which came as a json dump, organized into the `DatasaurDocument` class.

> "I need a list of all documents with truncated clause labels in them."

```python
$ python
>>> # Import the list of all transcript numbers
>>> from utils.data.datasaur import docs
>>> docs
[DatasaurDocument(2009_147.txt, s1036-42_s2008-9_s3000-15-NTliMzIxODk),
 DatasaurDocument(037_458.txt, s1036-42_s2008-9_s3000-15-NTliMzIxODk),
 DatasaurDocument(036_439.txt, s1036-42_s2008-9_s3000-15-NTliMzIxODk),
 DatasaurDocument(2009_148.txt, s1036-42_s2008-9_s3000-15-NTliMzIxODk),
 ...,
 DatasaurDocument(041_499.txt, s1036-42_s2008-9_s3000-15-NTliMzIxODk)]
>>> len(docs) # Now, if you're curious about how many docs there are
1226
>>>
```

> How many of these documents are from the Hoarding set (set 1)?

```python
>>> len([doc for doc in docs if doc.set == 1])
734
```
See the documentation on the `DatasaurDocument` class from the `document` module to see what else you can do when looking at this list.

## Transcripts

> "How many Interview Transcripts are in this Data?"

```python
$ python
>>> # Import the list of all transcript numbers
>>> from utils.transcript import transcript_numbers
>>> len(transcript_numbers)
84
>>> 
>>> # If you wanted to do this directly
```

Here are some example use cases of how to use the utils module.

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

## `document`

The `document` module contains two classes that are designed to make it easy for users to split the data for a particular document into Interviewer and Participant data.
This module contains two classes for this purpose:

- `BaseDocument`
- `TextDocument`
- `DatasaurDocument`

## `data`

If you're here, the `data` module is likely going to contain most of what you're going to care about.
It is a submodule of `utils` that is designed to allow for querying of the data.

`data` itself has two submodules:
- `datasaur`
- `raw`

Each submodule is designed to query the datasaur data—the data containing the manually labeled truncated clauses—and the raw text data, respectively.

### `datasaur`

The most important thing that this module has is the `docs` variable: this contains a list of every single document.
