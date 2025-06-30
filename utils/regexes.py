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

# This regex is used to match timestamps, i.e. '19:24', '3:14', or '12:34:56'.
# Also allows for ranges, i.e. '1:23-1:56'.
timestamps = re.compile(r'\d{1,2}[:;]\d{2}(?:[:;]\d{2})?\s?')
timestamps = re.compile(r'{ts}(?:-{ts})?'.format(ts=timestamps.pattern))
timestamps = re.compile(r'{ts}|\({ts}\)|\[{ts}\]'
                        .format(ts=timestamps.pattern))

extractable_token = re.compile(r"""(?:\((?:(\w*),?\s+)?{ts}\))|
                                   (?:\[(?:(\w*),?\s+)?{ts}\])
                                """.format(ts=timestamps.pattern),
                               flags = re.IGNORECASE | re.VERBOSE)