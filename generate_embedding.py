import pandas as pd
from tqdm import tqdm
import utils.datasaur as data
import utils.ling as ling
import utils.regexes as regexes
from utils.transcript import Transcript
from sentence_transformers import SentenceTransformer
from sqlitedict import SqliteDict

import statistics as stats

# Load the model
model = SentenceTransformer(
    "Qwen/Qwen3-Embedding-8B",
    model_kwargs={"device_map": "auto"}
)

# For CUDA machines maybe?
# model = SentenceTransformer(
#     "Qwen/Qwen3-Embedding-8B",
#     model_kwargs={"attn_implementation": "flash_attention_2", "device_map": "auto"},
#     tokenizer_kwargs={"padding_side": "left"},
# )

if __name__ == "__main__":
    # Cache DB
    db = SqliteDict("./out/embedding_cache.db")

    # List of rows in the csv file 
    sentence_pair_rows = []
    call_response_rows = []
    call_response_per_transcript_rows = []
    call_response_per_transcript_long_rows = []

    pbar = tqdm(data.by_transcript)
    for num in pbar:
        call_response_transcript_rows = []

        tr = Transcript(num)
        
        pbar.set_description(f"{num}")

        lines = []
        for doc in tr.docs:
            new_lines = [[doc.lines[i], doc._row_speakers_default[i], doc.name] for i in range(len(doc.lines))]
            # Remove Speaker Labels
            new_lines = [[regexes.speaker_labels_restricted.sub('', line[0]), line[1], line[2]] for line in new_lines]
            # Remove timestamps from the lines (and apply lowercase)
            new_lines = [[regexes.timestamps.sub('', line[0]).strip().lower(), line[1], line[2]] for line in new_lines]
            # Replace bracketed stuff with better representations
            new_lines = [[regexes.replace_tokens(line[0]), line[1], line[2]] for line in new_lines]
            # Remove tokens that are not useful for us
            new_lines = [[regexes.remove_tokens(line[0]), line[1], line[2]] for line in new_lines]
            # Remove empty lines
            new_lines = [line for line in new_lines if line[0]]

            lines.extend(new_lines)
        
        embeddings = [None for i in range(len(lines))]

        unencoded = []
        unencoded_map = []
        for i in range(len(lines)):
            # If line in cache, use it
            if lines[i][0] in db:
                print("Cache Hit: ", lines[i][0])
                embeddings[i] = db[lines[i][0]]
            else:
                # Otherwise, add it to the encode queue
                unencoded.append(lines[i][0])
                unencoded_map.append(i)
        
        unencoded_embeddings = model.encode(unencoded, show_progress_bar=True)

        # Map the unencoded embeddings back to their original indices
        for i, embedding in zip(unencoded_map, unencoded_embeddings):
            embeddings[i] = embedding
            # Store in cache
            db[lines[i][0]] = embedding

        similarity = model.similarity(embeddings, embeddings)

        # Create Call-Response rows
        for i in range(len(lines) - 1):
            if lines[i][1] == 'Interviewer' and lines[i + 1][1] == 'Participant':
                row = {
                    'Project': tr.number,
                    'Document Name': lines[i][2],
                    'Hoarder Flag': tr.docs[0].hoarder_flag,  # Assuming all docs have the same hoarder flag
                    'Similarity': similarity[i][i + 1].item(),
                    'Call': lines[i][0],
                    'Response': lines[i + 1][0]
                }
                call_response_transcript_rows.append(row)
                call_response_rows.append(row)

        # OLD
        interviewer_tokens = doc.tokens("Interviewer", flat=True) # type: ignore
        participant_tokens = doc.tokens("Participant", flat=True) # type: ignore

        mean = stats.mean([row["Similarity"] for row in call_response_transcript_rows])
        std = stats.stdev([row["Similarity"] for row in call_response_transcript_rows])

        mean_long = stats.mean([row["Similarity"] for row in call_response_transcript_rows if len(row["Call"]) > 10 and len(row["Response"]) > 10])
        std_long = stats.stdev([row["Similarity"] for row in call_response_transcript_rows if len(row["Call"]) > 10 and len(row["Response"]) > 10])

        row = {
            'Project': tr.number,
            'Hoarder Flag': tr.docs[0].hoarder_flag,
            'Mean': mean,
            'Std': std,
        }
        call_response_per_transcript_rows.append(row)

        row = {
            'Project': tr.number,
            'Hoarder Flag': tr.docs[0].hoarder_flag,
            'Mean': mean_long,
            'Std': std_long,
        }
        call_response_per_transcript_long_rows.append(row)

        row = { 
            'Project' : doc.project,
            'Document Name' : doc.name, 
            'Hoarder Flag' : doc.hoarder_flag,
            **doc.label_counts,
            'TTR-Interviewer' : ling.type_token_ratio(interviewer_tokens),
            'TTR-Participant' : ling.type_token_ratio(participant_tokens),
            'TTR-sent-Interviewer' : ling.type_token_ratio(interviewer_tokens),
            'TTR-sent-Participant' : ling.type_token_ratio(participant_tokens),
            'ASL-Interviewer' : ling.average_sentence_length(
                doc.tokens("Participant")), # type: ignore
            'ASL-Participant' : ling.average_sentence_length(
                doc.tokens("Interviewer")), # type: ignore
        }
        sentence_pair_rows.append(row)

        db.commit()

    db.close()
    
    sp_df = pd.DataFrame(sentence_pair_rows)
    sp_df.to_csv('./out/embedding_sentence_pair_table.csv', index=False)
    cr_df = pd.DataFrame(call_response_rows)
    cr_df.to_csv('./out/embedding_call_response_table.csv', index=False)
    cr_per_transcript_df = pd.DataFrame(call_response_per_transcript_rows)
    cr_per_transcript_df.to_csv('./out/embedding_call_response_per_transcript_table.csv', index=False)
    cr_per_transcript_long_df = pd.DataFrame(call_response_per_transcript_long_rows)
    cr_per_transcript_long_df.to_csv('./out/embedding_call_response_per_transcript_long_table.csv', index=False)