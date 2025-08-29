# How to replicate our data cleaning

You may notice some Python scripts in the repository that are unrelated to analyzing the data. 
These scripts are meant to modify the data for cleaning.
Though most data cleaning is done in-memory, we modified some parts of the data itself in the project in order to fix some issues that we felt required direct modification.
In this document, we will show the process in which the data was modified and why for replication and documentation purposes.

## Transcript and Document Numbering Scheme

Interviews were recorded as whole *transcripts*, i.e. an interview with Participant "John Doe" would may been recorded as *transcript* `005`.
Note that the transcript number's first digit indicates whether it was an interview with a hoarding patient or not.
If it is a zero, like with `005`, then the transcript is an interview with a hoarding patient.  
Otherwise, if it is a 2 or a 3, like `2005` or `3005`, then the transcript is from an interview that is from one of the control data sets.

After this, transcripts were divided into multiple pieces, which we called *documents*, which were used for analysis.
For instance, document `005_027` would be a small excerpt from transcript `005`.
Unfortunately, the document numbering convention wasn't entirely clear. 
`005_027` may not necessarily be the 27th division of transcript `005`---it may be the 1st division, the 2nd division, the 33rd division, etc. 
The only thing we do know is that if the documents `005_027` and `005_028` exist, then the content from `005_028` necessarily comes after the content from `005_027`. But even then, it may not be directly after. A mock example (not actual data):
```
--- Transcript 005 mock content
...
--- BEGIN DOCUMENT 005_027 ---
28 Interviewer: What's Hoarding like for you?
29 Participant: It's ok.
30 Interviewer: Can you tell me more?
--- END DOCUMENT 005_027 ---
31 Participant: Well, I manage. It's stressful having so much... being around so much stuff. But I manage.
32 Interviewer: What's it like on your family?
--- BEGIN DOCUMENT 005_028 ---
33 Participant: They get really frustrated. My son always complains when he comes home.
34 Interviewer: What in particular does he complain about?
35 Participant: Not being... not being able to walk in the bathroom.
--- END DOCUMENT 005_028 ---
...
```
(The mock comments, inscribed by `---`, would not be present in the transcript).
So, as we see, the content from document `005_028` necessarily comes after the content from `005_027`, but some content—in this case, lines 31-32—may be missed in between. This isn't always the case, but it's frequent.

## The Scripts: What they fix

If you want to replicate the data fixing, run the scripts in the order that the headings are presented here.
Run all scripts from the project's root.
Note that we fully acknowledge that some of these fixes could have been implemented in code while analyzing the data in-memory:
we simply did not because we were exhausted, and somehow this felt easier.
Don't ask why!

### `fix_transcript_012.py`

In this transcript, every label that said `Interviewee:` should have actually said `Interviewer:`. 
This script fixes that.

### `deidentify.py`

This script replaces identifying information with generic names. For instance, "Jane" would be replaced with "NAME", "New York City" would be replaced with "CITY", etc.

### `fix_transcripts_001-007.py`

This script checks all documents from the transcripts `001` to `007` for renaming. 
More accurately, it fixes all documents that are said to be from that range—some of these documents are actually from transcripts `2001` to `2007`.
This is a big deal: which means that some documents from control transcripts are labeled as hoarding transcripts, which can mess up classification (which relies on the document name's first digit).

We checked in `001-007_fixes.ipynb` that not a single document in any of the projects labeled HD_set1 have speakers that are labeled `"Interviewee"`. 
Thus, assuming that all documents in HD_set1 are actually hoarding documents, this is sufficient evidence to conclude that if a document has a speaker labeled "Interviewee", it is not a hoarding document, and is in fact from transcripts `2001` to `2007` and not `001` to `007`.

### `fix_transcript_2005.py`

This transcript had mismatched speakers: "P3" should have been "Interviewee" and vice versa.
This script should not be run until after the previous script, otherwise not all documents from `2005` will be targeted.

### `remove_duplicates.py`

This script looks for documents with identical names and identical content, and chooses one of the documents at random to remove.
We choose to run this after `fix_transcripts_001-007.py` so that names are accurate.

### `fix_misspellings.py`

Fixes known misspellings of speaker labels found across documents. 

### `fix_059_718.py`

This line is in this document:

```
Interviewer19:09- Ok sounds good.
```

This script just fixes that.

### `fix_timestamps.py`

Fixes issues with timestamps looking like `07 :08` and `34:4o`.