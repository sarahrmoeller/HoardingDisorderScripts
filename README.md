# Scripts for Running Statistics on Hoarding Disorder Data

Here reside the scripts for running Statistics on the data we have on Hoarding Disorder patients and control, 
including labeled data from datasaur and the original unlabeled data (TBD). 

## Replicating Our Work

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
Run `python generate_label_counts.py` to generate the file `label_counts.csv` located in the `./out/` directiory. Each row in this file specifies a file,
the set it came from, and provides a "hoarding flag" (1 if hoarding patient, 0 otherwise), the number of labels of each type in the file, as well as
the total label counts in the file.

Create an interactive R session with the file `log-reg.r` to see the logisitc models. We created four models, numbered `mdl1`, ..., `mdl4`:

1. A multiple logistic regression (MLR) model against counts of all label types in each document (we exclude the total label count in this model to avoid multicollinearity).
2. A simple logistic regression model on total label counts in each document.
3. A MLR model against counts of all label types except for Misspeak and Unclear. We created this model because these predictors had high standard errors in the first model,
   so we hoped that taking away these labels would improve the model's prediction.
4. A MLR model against counts of all label types except for Misspeak, Unclear, and Self Correction. We removed Self Correction from this model as its p-value was high in
   previous models.
