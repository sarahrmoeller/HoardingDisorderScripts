import pytest
from utils import regexes 


@pytest.mark.parametrize("input_line,expected", [
    # Basic speaker labels
    ("Interviewer:", ["Interviewer"]),
    ("Participant:", ["Participant"]),
    ("Rebecca:", ["Rebecca"]),
    ("Interviewee:", ["Interviewee"]),
    ("Speaker:", ["Speaker"]),
    ("P1:", ["P1"]),
    ("P3:", ["P3"]),
    # Speaker with number
    ("Participant 12:", ["Participant"]),
    ("Interviewer 2:", ["Interviewer"]),
    # Speaker with timestamp
    ("19:24 Interviewer:", ["Interviewer"]),
    ("23:14 Participant:", ["Participant"]),
    # No speaker
    ("Random text", []),
    ("23:27", []),
    (":", []),
    (" : ", []),
    # Speaker with extra text
    ("Rebecca: How are you?", ["Rebecca"]),
    ("Interviewee: Fine.", ["Interviewee"]),
    ("P1: Okay, kind of inline with that", ["P1"]),
    ("P3: Hm hm, yeah that’s an", ["P3"]),
    # Multiple speakers in one line
    ("Interviewer: Participant:", ["Interviewer", "Participant"]),
    ("P1: P3: Something", ["P1", "P3"]),
    # Speaker with number and text
    ("Interviewer 3: Hello", ["Interviewer"]),
    ("Participant 7: Hi", ["Participant"]),
    # Test arbitrary whitespace between numbers
    ("Participant  004: ", ["Participant"]),
    ("Participant\t004: ", ["Participant"]),
    ("Participant \t004: ", ["Participant"]),
    # Make sure we don't match some of the weird cases we've found
    ("[:", []),
    ("]:", []),
    ("[0:", []),
    ("PART 2 OF 4 ENDS [00:46:04]", []),
    ("This is NAME [00:02] again", []),
    ("Rebecca: Hi NAME [00:01] how are you?", ['Rebecca']),
])
def test_speaker_labels(input_line, expected):
    assert regexes.speaker_labels.findall(input_line) == expected


@pytest.mark.parametrize("string,expected", [
    ("17:38", ""),
    ("1:23", ""),
    ("12:34:56", ""),
    ("1:52:23", ""),
    ("1;23", ""), # Mistakes allowed
    ("1:23-1:56", ""), # Ranges allowed
    ("2:23 Interviewer:", " Interviewer:"),
    # Test with brackets/parentheses
    ("(17:38)", ""),
    ("(1:23)", ""),
    ("(12:34:56)", ""),
    ("(1:52:23)", ""),
    ("[17:38]", ""),
    ("[1:23]", ""),
    ("[12:34:56]", ""),
    ("[1:52:23]", ""),
    ("[1:52:23-12:43:44]", ""),
])
def test_timestamps(string, expected):
    assert regexes.timestamps.match(string)
    assert regexes.timestamps.sub('', string) == expected


@pytest.mark.parametrize("string,expected", [ 
    ("(NAME)", "NAME"),
    ("[NAME]", "NAME"),
    ("(inAuDiBlE 2:23)", "INAUDIBLE"),
    ("[inAuDiBlE 2:23]", "INAUDIBLE"),
    ("(NAME, 2:23)", "NAME"), 
    ("[NAME, 2:23]", "NAME"),
    ("(UNIVERSITY, (2:24))", "UNIVERSITY"), # Try with timestamp's parentheses
    ("[UNIVERSITY, (2:24)]", "UNIVERSITY"),
    ("(UNIVERSITY, [2:25])", "UNIVERSITY"), # And with timestamp brackets
    ("[UNIVERSITY, [2:25]]", "UNIVERSITY"),
    ("[names of companies; (48:15)]", "NAMES_OF_COMPANIES"),
    # Dedacted
    ("[NAME DEDACTED]", "NAME"),
    ("[NAME REDACTED]", "NAME"),
    # In context
    ("When we go to the [inaudible 2:23] place", 
     "When we go to the INAUDIBLE place"), 
])
def test_extractable_token(string, expected):
    assert regexes.extractable_token.search(string)
    assert regexes.replace_tokens(string) == expected


@pytest.mark.parametrize("string", [
    "001",
    "Interview 001",
    "PART 2 of 4 ENDS (12:34:56)",
    "[END OF RECORDING]",
    "(affirmative)",
    "(negative)",
])
def test_removable_token(string):
    assert regexes.remove_tokens(string) == ""