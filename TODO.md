# TODO

- [ ] Important:
  - [x] Create Logistic Model
  - [x] Abstract `generate_table.py` code into `Document` class
  - [ ] Separate document content into interviewer and participant
    - [ ] Implement row speaker detection:
      - [ ] Figure out what to do with three-speaker documents
      - [ ] WARN ABOUT SPEAKERS NOT AT THE BEGINNING OF THE LINE!!!
  - [ ] Identify removable tokens in documents, i.e. timestamps (i.e. 18:19, (18:19), (1:25:01)), [END OF RECORDING], [TRANSCRIPT PAUSED], variations of INAUDIBLE (??), etc.
  - [ ] Implement metrics from previous paper:
    - [ ] Type-Token Ratio
    - [ ] Average Sentence Length
    - [ ] Noun Phrase (NP) Count/Ratio
  - [ ] Report model accuracy
- [ ] Later:
  - [ ] Frankenstein Document content together
    - [ ] Create new table based on Frank. Documents
  - [ ] Speech Graphs???
  - [ ] Find way to automatically label incomplete clauses
