# TODO
Create a “clean” version of set 1, 2 and 3. Once cleaned, rename folders and files of “noisy” sets to keep separate.
- [ ] Important:
  - [x] Create Logistic Model
  - [x] Abstract `generate_table.py` code into `Document` class
  - [x] Fix broken transcripts found in `broken_transcripts.ipynb`
    - [x] 2010
    - [x] 012
    - [x] 001-007
  - [x] Separate document content into interviewer and participant
    - [x] Figure out what to do with three-speaker documents (we are doing Frankenstein to solve this)
    - [x] ~~Frankenstein Document content together to analyze data by Transcript~~ Create `Transcript` class
    - [x] Create new table based on transcript data
    - [x] Identify certain lines that don't need speaker labels, i.e. transcript labels, [END OF RECORDING], and PART 2 OF 4 ENDS [00:46:04] (look through removable tokens), see `identifying_removable_tokens.ipynb`
Later:
  - [ ] Implement metrics from previous paper using cleaned text files
  - [ ] Cohen's Kappa
  - [ ] Report model accuracy
  - [ ] Find way to automatically label incomplete clauses
-
