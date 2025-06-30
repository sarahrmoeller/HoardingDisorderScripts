# TODO

- [ ] Important:
  - [x] Create Logistic Model
  - [x] Abstract `generate_table.py` code into `Document` class
  ~~- [ ] Fix Transcript no. 005~~
  - [x] Fix broken transcripts found in `broken_transcripts.ipynb`
    - [x] 2010
    - [x] 012
    - [x] 001-007
  - [ ] Separate document content into interviewer and participant
    - [x] Figure out what to do with three-speaker documents (we are doing Frankenstein to solve this)
    - [x] ~~Frankenstein Document content together to analyze data by Transcript~~ Create `Transcript` class
    - [x] Create new table based on transcript data
    - [x] Identify certain lines that don't need speaker labels, i.e. transcript labels, [END OF RECORDING], and PART 2 OF 4 ENDS [00:46:04] (look through removable tokens), see `identifying_removable_tokens.ipynb`
    - [ ] WARN ABOUT SPEAKERS NOT AT THE BEGINNING OF THE LINE!!!
  - [ ] Clean documents:
    - [x] Identify removable tokens in documents (see `identifying_removable_tokens.ipynb`)
    - [ ] Figure out how to remove each removable token
    - [ ] Edit `Document` class to include a cleaned version
  - [ ] Implement metrics from previous paper:
    - [ ] Type-Token Ratio
      - [ ] Document TTR
      - [ ] Average Sentence TTR
      - [ ] Average Sentence Length
      - [ ] Noun Phrase (NP) Count/Ratio
Later:
  - [ ] Report model accuracy
  - [ ] Speech Graphs???
  - [ ] Find way to automatically label incomplete clauses
