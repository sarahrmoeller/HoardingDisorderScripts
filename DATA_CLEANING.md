# Data Cleaning

After importing the label data from datasaur, we needed to apply a few changes to the text data after realizing that a few things were off with the text.
This file explains the changes we made and why.

If you want to replicate the data fixing, simply run `python fix_truncated_clause_data.py`.

## Review: Transcript and Document Numbering Scheme

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

## What We Fixed

### Speaker Label Correction

#### Fix Transcript 012 speaker labels

In Transcript 012, the speaker label "Interviewee" was mistakenly labeled as "Interviewer". 
This code corrects that error by replacing all instances of "Interviewee" with "Interviewer".

#### Deidentification

This script replaces identifying information with generic names. For instance, "Jane" would be replaced with "NAME", "New York City" would be replaced with "CITY", etc.
Most importantly, this script also deidentifies speakers: this is necessary for speaker label deidentification.

#### Fix Misspelled Labels

Fixes a number of miscellaneous issues relating to speaker labels being misspelled or miswritten in some way.

#### Fix Label in Document 3001_039.txt

We just change "Interviewer:Right" to "Interviewer: Right" in this document. 
This is necessary for speaker label detection, as the regex that detects speaker labels assumes that they are separated from the next word via whitespace.
As far as we could tell, this was the only instance of this mistake happening across the data (yes, we checked this multiple times).

### Fix Transcripts 001-007

This script checks all documents from the transcripts `001` to `007` for renaming (not including 004). 
More accurately, it fixes all documents that are said to be from that range—some of these documents are actually from transcripts `2001` to `2007`.
This is a big deal: which means that some documents from control transcripts are labeled as hoarding transcripts, which can mess up classification (which relies on the document name's first digit).

We checked in `001-007_fixes.ipynb` that not a single document in any of the projects labeled HD_set1 have speakers that are labeled `"Interviewee"`. 
Thus, assuming that all documents in HD_set1 are actually hoarding documents, this is sufficient evidence to conclude that if a document has a speaker labeled "Interviewee", it is not a hoarding document, and is in fact from transcripts `2001` to `2007` and not `001` to `007`.

### Remove Duplicates

We then proceed to find pairs of documents in the data that have the same name, and pick one at random to delete.

### Fix Transcript 2005: Swap "P3" and "Interviweee" Labels

Transcript 2005 had mismatched speakers: "P3" should have been "Interviewee" and vice versa.

### Final Cleaning Documentation / TODO list

- [ ] Fix Text Data (to the best of our ability, for now)
  - [ ] Remove from every document transcriber notes that don’t stand in for words: 
    - [x] Timestamps, 
    - [x] Identify removable tokens in documents (see `identifying_removable_tokens.ipynb`)
      - [ ] Transcript-related details (INTERVIEW 001), [PAUSED], [END OF RECORDING] 
      - [x] [affirmative], [negative], [laughter], etc.
    - [ ] Figure out how to remove each removable token (see `./utils/regexes.py`, lines 88-108)
      - [ ] Make separate regex to filter transcript-related details
  - [x] Make sure anonymization and other transcriber notes that need to be kept because they substitute words are marked with identical format for same types of things, e.g. [ANONYMIZATION], [ORGANIZATION], [NAME], [INAUDIBLE]. Format exactly the same in every document the anonymization and unclear comments in square brackets and capital letters. Same as old note "Normalize certain tokens, i.e. LOCATION == CITY, STATE, ETC" 
  - [x] Make speaker labels homogeneous: all interviewers and interviewees notated the same when in "{Speaker Label}:" format.
    - [x] Edit `Document` class to include a cleaned version
    - [x] Test Document cleaning on specific Documents
- [x] Figure out what to do about speakers that are not at the beginning of the line
- [ ] Manual Work, check for:
  - [ ] Consistently formatted speaker labels <Label(#):_> Interviewer: or Interviewer1: or Interviewer2: Interviewee: 
  - [ ] Make sure that interviewer/interviewee are correctly labeled, especially when there is more than two speakers.
  - [ ] Keep these transcriber notes. Put them on their own line. Put square brackets around them. 
        [Interview 001] 
        [END OF RECORDING]
        [PAUSED]
- [ ] Remove any transcriber notes that do not stand in for an utterance, such as:
      time stamps
      [laughter]
      [affirmative]
      [negative]
- [ ] Keep that the transcriptionists' notes that represent anonymized or inaudible speech. Put in all caps, make them consistent (at least across sets).
      ANONYMIZATION
      ORGANIZATION
      NAME 
      INAUDIBLE
This script should not be run until after transcripts `001`-`007` are fixed, otherwise not all documents from `2005` will be targeted.

### Fix Timestamps

We then fixes issues with timestamps looking like `07 :08` and `34:4o` in a number of specific documents.
