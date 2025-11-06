"""
This script will take each raw document file and clean out speaker labels and
timestamps.

What's a bit hilarious about this is that the way I'm going to do this is not
by cleaning the raw files directly, but by using the existing `Document` class,
in the `utils` module, which is designed to handle the data in json format, 
and use its inherent functions to extract the text from the json files and 
automatically clean it, then write those files to txt. 
"""
from pathlib import Path
import utils.datasaur as data
from utils.datasaur import base_data_folder_name


for doc in data.by_doc:
    content = doc.content_by_speaker('Participant')
    
    # Create directory and write file
    cleaned_path = Path(
        f'./{base_data_folder_name}/cleaned/set0{doc.set}/{doc.name}')
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_path.write_text(content)
    
    # Also writing to ./for_punkt_mdl/ for a flat list
    training_path = Path(
        f'./{base_data_folder_name}/for_punkt_mdl/{doc.name}')
    training_path.parent.mkdir(parents=True, exist_ok=True)
    training_path.write_text(content)