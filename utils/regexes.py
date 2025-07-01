import re


# List of Interviewer/Participant speaker name tuples found in the data.
# We commented to the right which set the pair was found in.
# We use the convention that the last speaker in the tuple is the participant,
# and all other speakers are interviewers.
SPEAKER_PAIRS: list[tuple] = [
    ("Interviewer", "Participant"), # Hoarding-Patient (set 1)
    ("Interviewer", "Interviewee"), # Hoarding-Clinician (set 2) & Transcript no. 012
    ("Interviewer", "Speaker"), # Parents (set 3)
    ("P1", "P3", "Interviewee"), # Transcript no. (2)005
    ("P1", "P2", "Interviewee") # Transcript no. 2008
]
SPEAKERS: set = {speaker for pair in SPEAKER_PAIRS for speaker in pair}


# This regex is used to match speaker labels, i.e. 'Interviewer:', 
# 'Participant 12:', 'Spongebob: '. Any attempt to match a speaker label
# will return the label itself, e.g. finding 'Interviewer:' in the text 
# returns 'Interviewer'
speaker_labels = re.compile(r'([a-zA-Z][a-zA-Z0-9]+)(?:\s+\d+)?:')
# This regex is used to match only speaker labels that are found in the 
# SPEAKERS set.
speaker_labels_restricted = re.compile(r'\s*(?:{speakers})(?:\s+\d+)?:\s*'
                                       .format(speakers='|'.join(SPEAKERS)))

def find_speakers(content: str, restrict=True) -> list[str]:
    """
    Takes in a string (`content`),
    Returns a list of all occurences of strings followed by optional 
    whitespace, optional number(s), and a colon. It then captures the 
    string. The format is:
        (captured string) [optional number]:
    If `restrict` is True, it only returns speakers that are in the 
    `SPEAKERS` set.

    Examples: 
    - 'Interviewer:' -> ['Interviewer']
    - 'Participant 12: ' -> ['Participant']
    - 'Spongebob:' -> [] (if `restrict` is True, since 'Spongebob' is not 
                            in `SPEAKERS`)
    """
    matches = speaker_labels.findall(content)
    if not restrict:
        return matches
    return [match for match in matches if match in SPEAKERS]

# This regex is used to match timestamps, i.e. '19:24', '3:14', or '12:34:56'.
# Also allows for ranges, i.e. '1:23-1:56'.
timestamps = re.compile(r'\d{1,2}[:;]\d{2}(?:[:;]\d{2})?')
timestamps = re.compile(r'{ts}(?:-{ts})?'.format(ts=timestamps.pattern))
timestamps = re.compile(r'\({ts}\)|\[{ts}\]|{ts}'
                        .format(ts=timestamps.pattern))


extractable_token = re.compile(r"([a-zA-Z ]+)(?:[,;]?\s+(?:{ts}))?"
                               .format(ts=timestamps.pattern))
extractable_token = re.compile(r"\({et}\)|\[{et}\]"
                               .format(et=extractable_token.pattern))

def replace_tokens(string: str) -> str:
    """
    Replaces all tokens in a string according to the extractable_token regex.
    If a token with spaces is found, it is joined together by underscores.
    
    Args:
        string (str): The string to extract the token from.
        
    Returns:
        str: The extracted token, in uppercase and with underscores 
             instead of spaces.
    """
    string = extractable_token.sub(lambda m: '_'.join((m.group(1) or 
                                                       m.group(2) or 
                                                       '').upper()
                                                          .split()),
                                   string)
    return string.replace('_REDACTED', '').replace('_DEDACTED', '')


removable_token_patterns = [
    r'^(Interview )?\d{3}$', # Matches '001', 'Interview 001' (only if this is the whole line)
    r'PART \d of \d ENDS {ts}'.format(ts=timestamps.pattern),
    r'\[END OF RECORDING\]', # Matches literal '[END OF RECORDING]'
    r'\(affirmative\)|\(negative\)' # Matches literal '[END OF RECORDING]'
]

def remove_tokens(string: str) -> str:
    """
    Removes all removable tokens from a string.
    
    Args:
        string (str): The string to remove the tokens from.
        
    Returns:
        str: The string with the tokens removed.
    """
    for pattern in removable_token_patterns:
        string = re.sub(pattern, '', string, flags=re.IGNORECASE)
    return string.strip()