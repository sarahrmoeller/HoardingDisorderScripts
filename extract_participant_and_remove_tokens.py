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
from utils.raw import text_files_dir


for doc in data.by_doc:
    content = doc.content_by_speaker('Participant')
    
    # Create directory and write file
    cleaned_path = Path(
        f'{text_files_dir}/cleaned/participant/{doc.name}')
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_path.write_text(content)