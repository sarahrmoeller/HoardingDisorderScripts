# Scripts for Running Statistics on Hoarding Disorder Data

Here reside the scripts for running Statistics on the data we have on Hoarding Disorder patients and control, 
including labeled data from datasaur and the original unlabeled data (TBD). 

## How to Replicate our Work

### Python Environment

These python scripts were run in a a python virtual environment with `venv`. To replicate our results, we recommend the following:
1. Check for `python` version 3.10.12 and `pip` version 22.0.2.
2. Clone our repository with `git` to your machine, and ensure you are in the root directory of the cloned repository.
3. Create a new virtual environment using `{path/to/python3} -m venv .venv`.
4. Run `source .venv/bin/activate` from the project's root directory to activate the virtual environment.
5. Run `pip install -r requirements.txt` to install all needed dependencies to replicate our work. 

We tested this on multiple computers with the given versions.  It may be possible to get our code working using `conda`/`anaconda`, but we have not tested this. 

### Data

To get same data we used for the experiments run in this project, ask one of us for the `data.zip` file. 
Unzip this file, and move its contents `data/` directory.  The project's file structure on your end should look like this:

```
HoardingDisorderScripts/
   .venv/
   data/
      HD-Set-1-7/
      HD-Set-8-11/
      ...
      .gitignore
   ... (other directories)
   data.zip
   README.md
   TODO.md
   ... (other files)
```

### Label Count Results

Our first test was to see whether the number of labels of each type in a document were significant in predicting Hoarding. To this end, we
created a logistic regression model each document's hoarding flag given the number of labels in each document.
Run `python generate_table.py` to generate the file `table.csv` located in the `./out/` directiory. Each row in this file specifies a file,
the set it came from, and provides a "hoarding flag" (1 if hoarding patient, 0 otherwise), the number of labels of each type in the file, as well as
the total label counts in the file. It also contains Type-token ratio (TTR) and Average Sentence Length (ASL) information.

Create an interactive R session with the file `log-reg.r` to see the logisitc models. 
We created a few models:

1. `total.slr`: Model predicting Hoarding against total label counts in a document.
2. `speaker.mlr`: Model predicting Hoarding against label counts, which are divided by type and speaker (of the label), the speakers being Interviewer or Participant.
3. `total.mlr`: Model predicting Hoarding against label counts, divided only by type.
