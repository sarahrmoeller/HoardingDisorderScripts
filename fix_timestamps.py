"""
The fixes here should be self-explanatory, given the context with the other
files.
"""
import utils.datasaur as data
from utils.transcript import Transcript
import json


# Found through datasaur diving
broken_timestamps = [
    # With spaces
    ('07: 27', '07:27', 4, ['3001', '030']),
    ('07: 27', '07:27', 23, ['3001', '048']),
    ('26: 35', '26:35', 14, ['2004', '053']),
    ('03: 58', '03:58', 9, ['3001', '082']),
    ('07: 34', '07:34', 1, ['3001', '083']),
    ('30: 31', '30:31', 5, ['3001', '087']),
    ('35: 11', '35:11', 9, ['3001', '088']),
    ('09: 22', '09:22', 9, ['059', '716']),
    ('34: 54', '34:54', 34, ['3001', '007']),
    ('38: 23', '38:23', 19, ['3001', '008']),
    ('26: 48', '26:48', 26, ['3001', '005']),
    ('03: 44', '03:44', 27, ['3001', '000']),
    ('41: 50', '41:50', 29, ['3001', '009']),
    ('43: 27', '43:27', 41, ['3001', '009']),
    ('31: 23', '31:23', 30, ['3001', '006']),
    ('[26: 35]', '[26:35]', 14, ['2004', '053']),
    ('09: 22-', '09:22-', 9, ['059', '716']),
    # With letters
    ('34:4y', '34:46', 44, ['054', '671']),
    ('36:4o', '36:40', 15, ['3001', '034'])
]


for broken_ts, fixed_ts, line_num, [trans_num, doc_num] in broken_timestamps: 
    doc = Transcript(trans_num)[doc_num]

    # Fix line
    doc.lines[line_num] = doc.lines[line_num].replace(broken_ts, fixed_ts)
    doc.row_data[line_num]['content'] = doc.lines[line_num]

    # Fix tokens
    token_line: list[str] = doc.tokens[line_num]
    if ' ' in broken_ts:
        # Special fix for broken timestamps with spaces
        broken_ts_parts = broken_ts.split()
        if any(part not in token_line for part in broken_ts_parts):
            continue
        fixed_token_index = token_line.index(broken_ts_parts[0])
        token_line[fixed_token_index] = fixed_ts
        del token_line[fixed_token_index + 1]
    else:
        # Normal fix
        try:
            index = [i for i in range(len(token_line)) 
                    if broken_ts in token_line[i]][0]
        except IndexError:
            continue
        token_line[index] = token_line[index].replace(broken_ts, fixed_ts)
    doc.row_data[line_num]['tokens'] = token_line

    doc.json_dump['rows'] = doc.row_data

    with open(data.review_dir(doc.project) + doc.name + '.json', "w") as f:
        json.dump(doc.json_dump, f)