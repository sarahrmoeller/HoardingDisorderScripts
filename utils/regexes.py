import re
from difflib import get_close_matches


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


def find_speaker_format_issues(text, speaker_set):
        """
       Method 2.1 Detects speaker label formatting issues:
            1. Speaker label followed by space before colon (e.g., 'Participant :')
            2. Speaker label followed by punctuation or character other than ':' (e.g., 'Participant.', 'Participant-')
        Returns a dictionary with issue types and matching instances.
        """
        issues = {}

        # Pattern 1: Space before colon "Participant :" (colon spacing issue)
        spacing_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(s) for s in speaker_set) + r')\s+:')
        spacing_matches = spacing_pattern.findall(text)
        if spacing_matches:
            issues['spacing_issue'] = spacing_matches

        # Pattern 2: Speaker label followed by something other than colon or space (e.g., 'Participant.' or 'Participant!')
        bad_punct_pattern = re.compile(r'\b(?:' + '|'.join(re.escape(s) for s in speaker_set) + r')[^\s:]')
        punct_matches = bad_punct_pattern.findall(text)
        if punct_matches:
            issues['bad_punctuation'] = punct_matches

        return issues


def find_spelling_variants(text, speaker_set, threshold=0.8):
    '''
    Method 3.1 Finds likely misspellings of speaker labels using fuzzy matching.
    '''
    pattern = re.compile(r'^([A-Z][a-zA-Z0-9_ ]{1,30})(?=\s*:\s*)', re.MULTILINE)
    candidates = pattern.findall(text)

    fuzzy_hits = {}
    for cand in candidates:
        matches = get_close_matches(cand, speaker_set, n=1, cutoff=threshold)
        if matches and matches[0] != cand:
            fuzzy_hits[cand] = matches[0]
    return fuzzy_hits


def find_multi_speaker_lines(text):
    '''
    Method 3.2 Finds lines that contain more than one speaker label.
    '''
    speaker_pattern = r'\b(?:' + '|'.join(re.escape(s) for s in SPEAKERS) + r')\s*:'
    pattern = re.compile(speaker_pattern)
    multi_speaker_lines = []
    for i, line in enumerate(text.splitlines()):
        matches = pattern.findall(line)
        if len(matches) > 1:
            multi_speaker_lines.append((i + 1, line.strip(), matches))
    return multi_speaker_lines


def find_speaker_at_end_of_line(text):
    """
    Method 3.3 Detect speaker labels that don't come after newlines.
    Ex:
        "Yeah, that's an interesting idea. Participant:"
    """
    pattern = re.compile(r'\b(?:{speakers})\s*:'
                         .format(speakers='|'.join(SPEAKERS)),
                         re.MULTILINE)
    return pattern.findall(text)