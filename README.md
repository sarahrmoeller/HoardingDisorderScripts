# Scripts for Running Statistics on Hoarding Disorder Data

Here reside the scripts for running Statistics on the data we have on Hoarding Disorder patients and control, 
including labeled data from datasaur and the original unlabeled data (TBD). 

## How to Replicate our Python Environment

These python scripts were run in a a python virtual environment with `venv`. To replicate our results, we recommend the following:
1. Clone our repository.
2. Check for `python` version 3.10.19 and `pip` version 26.0.1, then create a new virtual environment with these versions. We created our environment with `{path/to/python3} -m venv .venv`.
4. Run `source .venv/bin/{your activation script}` from the project's root directory to activate the virtual environment.
5. Run `pip install -r requirements.txt` to install all needed dependencies to replicate our work. 

We tested this on multiple computers with the given versions.  
It may be possible to get our code working using `conda`/`anaconda`, but we have not tested this. 
We are working to port our environment to nix.

## Project Structure

### Data

All data that is used for this project can be found in the `./data` folder. 
See `./data/mathews/documents/README.md` for a full explanation of the data.

### Code

#### For Those Reading The Paper

If you are looking to replicate our results and have little or no interest in looking directly at the nitty-gritty details of the data, look for `./logistic-regression.r`. 
This contains the code containing the model and numbers for the tables used in the paper's result section.
You'll also find the spreadsheets used for the model in the `./tables/` directory.

If you're coming from the poster session, `./forest.R` generates the forest plot for the data that was shown (its code may be outdated).

#### For Those Working More Deeply with The Code

If you are here, and finding yourself asking questions like "How many transcripts are in our data?" "How many documents does Transcript 2005 have?" "How transcripts are in set 3?" "Are there any duplicated documents?"
You will likely find that most—if not all—of what you will need to work with this project is in the `./utils/` directory.
This contains a number of functions and classes written in python useful for analyzing individual transcripts and documents, as well as making queries on a large number of documents.

#### Why Is It So Messy?

Due to limitations we encountered from the Python language, our root directory is littered with random `*.py` scripts in the root directory.
Ideally, we would have put a lot of these scripts in their own directories so things could be easier on the eyes, but the scripts in the root directory rely on the functions and classes within the `*.py` files in the `./utils/` directory.
To our knowledge, if we were to put the scripts you see in their own directories, python would consider these directories to be modules. 
Then, when the scripts attempt to use code from the `./utils/` directory, which to them would be some relative import like `../utils/`, python would forbid this as a rule against relative module importing. 
We have not found a clean workaround for this.
