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

