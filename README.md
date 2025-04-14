# Scripts for Running Statistics on Hoarding Disorder Data

Here reside the scripts for running Statistics on the data we have on Hoarding Disorder patients and control, 
including labeled data from datasaur and the original unlabeled data (TBD). 

## Replicating our Python Environment

These python scripts were run in a a python virtual environment with `venv`. To replicate our results, we recommend cloning our repository 
to your machine, and (after ensuring you are in the root directory of the cloned repository) creating a new virtual environment using `python -m venv .venv`.
After this, running `pip install -r requirements.txt` should install all needed dependencies to replicate our work. 

It may be possible to get our code working using `conda`/`anaconda`, but we have not tested this. 

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
