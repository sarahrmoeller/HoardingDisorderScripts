# `mathews/`

This directory contains all data related to the interview transcripts provided to us by Univeristy of Florida's Springhill hospital. 

## Background

We were provided with a total of 84 interview transcripts. 
58 of these interviews were with Hoarding patients, while 26 were with non-Hoarding patients.
We then assigned undergraduate annotators from the University of Florida to annotate these transcripts. 

However, we did not assign them to read the entire transcripts as they were.  To do so would be a monumental task, as many of the transcripts lasted longer than 90 minutes.
To remedy this, we decided to take each transcript and break them up into what we called *documents*: bite-sized pieces of transcripts that would be easier for annotators to annotate.

In `documents/text_files`, you'll see the documents organized by sets.
In `documents/datasaur_exports`

## Which Copy of The Data Do I Have, "Fixed" or "Unfixed"?

The data we received in its original state.

Note that this version of the data is not "fixed"—there were issues in the data set that we had to manually fix.
We kept this "unfixed" version for the sake of replication: this is the state of the data before any of the scripts designed for fixing are run.

## `mathews/documents/`

This directory contains all data relating to the interview transcripts provided by Dr. Mathews.
Currently only contains data related to documents (broken-up pieces of transcripts), and not full transcripts.

### `text_files/`

You'll see this directory contains four subdirectories, all of which contain text documents in the format looking like `{number}_{number}.txt` (if you see `001_000.docx`, ignore that).
The first three, referring to sets, are organized by transcript type:

- *Set 1*: Interviews with Patients with Hoarding Disorder (HD),
- *Set 2*: Interviews with HD Experts,
- *Set 3*: Interviews with Parents about CBT.

In the format `{number}_{number}.txt` for document names, the first `{number}` is the transcript number from which the document came from.
For instance, Document `001_001.txt` comes from Transcript `001`, and Document `005_046.txt` comes from Transcript `005`.

Note that the transcript number's first digit will tell you which set the document belongs to. 
If the transcript number starts with a

- `0`, like in `001` or `005`, then the transcript (resp. document) belongs to set 1;
- `2` or `3`, like in `2008` then the transcript belongs to set 2; 
- `3`, like in `3001`, then the transcript belongs to set 3.

#### `participant/`

The result of taking each document from the `raw/` folder and extracting only the Participant utterances, while also cleaning timestamps.
We did not bother to maintain the set structure, as the documents tell us which set they're in by their first character.

### `datasaur_exports/`

This contains exported Datasaur Schema (.json) data from annotation efforts on datasaur.
The `truncated_clauses/` subfolder contains data from the truncated clauses annotation effort from the Fall 2024-Spring 2025 semester. 
Each of its subfolders corresponds to a project.

There is a directory here named `listing/` that is empty for now. 
This corresponds to the listing annotation effort on datasaur, which has not yet been completed.
When annotation is completed, we will export the label data from datasaur to this folder, and it will have nearly identical structure to the `truncated_clauses/` folder.