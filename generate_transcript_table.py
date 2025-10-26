import pandas as pd
from tqdm import tqdm
from utils.transcript import Transcript
import utils.datasaur as data 


if __name__ == "__main__":
    table_rows = [
        { 
            'Transcript' : tr.number,
            'Hoarder Flag' : tr.hoarder_flag,
            **tr.label_counts_tr
        }
        for tr in tqdm(Transcript(num) for num in data.transcript_numbers) ]
    df = pd.DataFrame(table_rows)
    df.to_csv('./out/transcript_table.csv', index=False)