import pytest
from utils.document import Document
import math


test_files: list[tuple[str, str]] = [
    # First three are chosen from a project that has files from each of 
    # sets 1-3
    ("s1062_s2022-26_s3076-97", "062_745.txt"), 
    ("s1062_s2022-26_s3076-97", "2022_335.txt"), 
    ("s1062_s2022-26_s3076-97", "3001_090.txt"), # Contains a single line saying "[TRANSCRIPTION PAUSED]"
    # Misc files with special cases
    ("s1043-5_s2010-11_s3016-25", "049_606.txt"),
    ("s1_28-35_s2_4-7", "2005_083.txt"), # contains "P1: " and "P3: " interview/speaker format
    ("s1_28-35_s2_4-7", "2005_082.txt"),
    ("s1_28-35_s2_4-7", "2005_086.txt"),
    ("s1036-42_s2008-9_s3000-15", "2008_136.txt"),
    ("s1_21-27_s2_1-3", "026_307.txt"), # Contains only Interviewer label, as well as [END OF RECORDING]
]
test_docs = {filename: Document(f"./data/{project}/REVIEW/{filename}.json")
             for project, filename in test_files}


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
def test_find_speakers(input_line, expected):
    doc = test_docs["062_745.txt"] # Use dummy instance
    assert doc.find_speakers(input_line, restrict=False) == expected


@pytest.mark.parametrize("test_doc,expected_speaker_set", [
    pytest.param(test_docs["062_745.txt"], {'Interviewer', 'Participant'}, 
                 id="Test arbitrary set 1 doc"),
    pytest.param(test_docs["2022_335.txt"], {'Interviewer', 'Interviewee'}, 
                 id="Test arbitrary set 2 doc"),
    pytest.param(test_docs["3001_090.txt"], {'Interviewer', 'Speaker'}, 
                 id="Test arbitrary set 3 doc"),
    pytest.param(test_docs["049_606.txt"], {'Interviewer', 'Participant'}, 
                 id="Document that doesn't begin with a speaker label"),
    # Do this test after 005 documents are fixed
    # (test_docs[-2], {'Interviewee', 'P1', 'P3'}, id="Three-speaker document (Interviewers: P1 and P3)"),
    pytest.param(test_docs["2008_136.txt"], {'P2', 'Interviewee', 'P1'}, 
                 id="Three-speaker document (Interviewers: P1 and P2)"),
    pytest.param(test_docs["026_307.txt"], {'Interviewer'}, 
                 id="Contains only Interviewer label, as well as [END OF RECORDING]"), # 
])
def test_speaker_set(test_doc, expected_speaker_set):
    assert test_doc.speaker_set(restrict=True) == expected_speaker_set


@pytest.mark.parametrize("test_doc,expected_speakers", [
    pytest.param(test_docs["062_745.txt"], [ 
                'Interviewer', 'Interviewer',
                'Participant', 'Participant',
                'Interviewer', 'Interviewer',
                'Participant', 'Participant',
                'Interviewer', 'Interviewer',
                'Participant', 'Participant',
                'Interviewer', 'Interviewer',
                'Participant', 'Participant',
                'Interviewer', 'Interviewer',
                'Participant', 'Participant',
                'Interviewer', 'Interviewer',
            ], id="Test arbitrary set 1 doc"),
    pytest.param(test_docs["2022_335.txt"], ['Interviewer', 'Interviewee'], 
                 id="Test arbitrary set 2 doc"),
    pytest.param(test_docs["3001_090.txt"], [
        'Interviewer', 'Speaker',
        'Interviewer', 'Speaker',
        'Interviewer', 'Speaker',
        'Interviewer', 'Speaker',
        'Interviewer', 'Speaker',
        'Interviewer', 'Speaker',
        'Speaker',
        'Interviewer', 'Speaker',
        'Interviewer', 'Speaker',
        'Interviewer', 'Speaker',
    ], id="Test arbitrary set 3 doc"),
    pytest.param(test_docs["049_606.txt"], [
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant',
        'Interviewer', 'Interviewer', 'Interviewer', 'Interviewer', 
        'Interviewer',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant'
    ], id="Document that doesn't begin with a speaker label"),
    # Do this test after 005 documents are fixed
    # (test_docs[-2], [ 
    #     'Interviewee',
    #     'P1',
    #     'Interviewee',
    #     'P1',
    #     'P3',
    #     'Interviewee',
    # ]),
    pytest.param(test_docs["2008_136.txt"], [
        'P2',
        'Interviewee',
        'Interviewee',
        'P1',
        'Interviewee',
        'P2',
        'Interviewee',
        'P2',
        'Interviewee',
        'P2',
        'Interviewee',
        'P2',
        'Interviewee'
    ], id="Three-speaker document"),
    pytest.param(test_docs["026_307.txt"], [
        'Interviewer',
        'Interviewer',
        'Interviewer',
        'Interviewer',
    ], id="Contains only Interviewer label, as well as [END OF RECORDING]"), # 
])
def test_row_speakers(test_doc, expected_speakers):
    assert test_doc._row_speakers == expected_speakers


# Each of these tests are basically the same as the previous one, but
# with all interviewer names changed to 'Interviewer' and all participant names
# changed to 'Participant'. This is useful for testing the default speaker 
@pytest.mark.parametrize("test_doc,expected_speakers", [
    pytest.param(test_docs["062_745.txt"], [
        'Interviewer', 'Interviewer',
        'Participant', 'Participant',
        'Interviewer', 'Interviewer',
        'Participant', 'Participant',
        'Interviewer', 'Interviewer',
        'Participant', 'Participant',
        'Interviewer', 'Interviewer',
        'Participant', 'Participant',
        'Interviewer', 'Interviewer',
        'Participant', 'Participant',
        'Interviewer', 'Interviewer',
    ], id="Test arbitrary set 1 doc with default speakers"),
    pytest.param(test_docs["2022_335.txt"], ['Interviewer', 'Participant'],
                 id="Test arbitrary set 2 doc with default speakers"),
    pytest.param(test_docs["3001_090.txt"], [
        'Interviewer', 'Participant',
        'Interviewer', 'Participant',
        'Interviewer', 'Participant',
        'Interviewer', 'Participant',
        'Interviewer', 'Participant',
        'Interviewer', 'Participant',
        'Participant',
        'Interviewer', 'Participant',
        'Interviewer', 'Participant',
        'Interviewer', 'Participant',
    ], id="Test arbitrary set 2 doc with default speakers"),
    pytest.param(test_docs["049_606.txt"], [
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant',
        'Interviewer', 'Interviewer', 'Interviewer', 'Interviewer', 
        'Interviewer',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant',
        'Participant', 'Participant', 'Participant', 'Participant'
    ], id="Document that doesn't begin with a speaker label"),
    pytest.param(test_docs["2008_136.txt"], [
        'Interviewer',
        'Participant',
        'Participant',
        'Interviewer',
        'Participant',
        'Interviewer',
        'Participant',
        'Interviewer',
        'Participant',
        'Interviewer',
        'Participant',
        'Interviewer',
        'Participant'
    ], id="Three-speaker document"),
    pytest.param(test_docs["026_307.txt"], [
        'Interviewer',
        'Interviewer',
        'Interviewer',
        'Interviewer',
    ], id="Contains only Interviewer label, as well as [END OF RECORDING]")
])
def test_row_speakers_default(test_doc, expected_speakers):
    assert test_doc._row_speakers_default == expected_speakers


@pytest.mark.parametrize("test_doc,expected", [
    (doc, None) for doc in test_docs.values()
])
def test_average_sentence_length(test_doc, expected):
    # If expected is None, just check that the value is a positive float
    # I.e. non-zero
    asl = test_doc.average_sentence_length
    assert isinstance(asl, float)
    assert asl > 0
