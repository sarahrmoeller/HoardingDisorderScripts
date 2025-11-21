# `./data/mathews/documents` 

The `./data` directory contains all of the data related to the HD research project.
As of now, the only data we have is under `mathews/documents`.
This directory contains all data related to the interview transcripts provided to us by Univeristy of Florida's Springhill hospital, all in document format (broken-up pieces of transcripts), and not full transcripts.

## Background

We were provided with a total of 84 interview transcripts. 
58 of these interviews were with Hoarding patients, while 26 were with non-Hoarding patients.
We then assigned undergraduate annotators from the University of Florida to annotate these transcripts. 

However, we did not assign them to read the entire transcripts as they were.  To do so would be a monumental task, as many of the transcripts lasted longer than 90 minutes.
To remedy this, we decided to take each transcript and break them up into what we called *documents*: bite-sized pieces of transcripts that would be easier for annotators to annotate.

In `documents/text_files`, you'll see the documents organized by sets.
In `documents/datasaur_exports`

## What are the directories?

### `text_files/`

You'll see this directory contains three subdirectories, all of which contain text documents in the format looking like `{number}_{number}.txt`.
These are organized by set:

- *Set 1*: Interviews with Patients with Hoarding Disorder (HD),
- *Set 2*: Interviews with HD Experts,
- *Set 3*: Interviews with Parents about CBT.

In the format `{number}_{number}.txt` for document names, the first `{number}` is the transcript number from which the document came from.
For instance, Document `1001_001.txt` comes from Transcript `1001`, and Document `1005_046.txt` comes from Transcript `1005`.

Note that the transcript number's first digit will tell you the set number the document belongs to. 
For instance, `1001_001.txt` and `1005_046.txt` both belong to set 1, `2005_087.txt` belongs to set 2, and so on.

### `datasaur_exports/`

This contains exported Datasaur Schema (.json) data from annotation efforts on datasaur.
The `truncated_clauses/` subfolder contains data from the truncated clauses annotation effort from the Fall 2024-Spring 2025 semester. 
Each of its subfolders corresponds to a project from the datasaur annotation.
As of now, this directory should be empty: we plan to fill it soon.

There is a directory here named `listing/` that is empty for now. 
This corresponds to the listing annotation effort on datasaur, which has not yet been completed.
When annotation is completed, we will export the label data from datasaur to this folder, and it will have nearly identical structure to the `truncated_clauses/` folder.