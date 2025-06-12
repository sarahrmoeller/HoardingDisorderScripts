# TODO

- [ ] Important:
  - [x] Create Logistic Model
  - [x] Abstract `generate_table.py` code into `Document` class
  - [ ] Separate document content into interviewer and participant
    - [ ] Implement row speaker detection:
      - [ ] Figure out what to do with three-speaker documents
      - [ ] WARN ABOUT SPEAKERS NOT AT THE BEGINNING OF THE LINE!!!
      - [ ] Identify certain lines that don't need speaker labels, i.e. transcript labels and 
            [END OF RECORDING]
  - [x] Identify removable tokens in documents:
  - [ ] Clean documents
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
