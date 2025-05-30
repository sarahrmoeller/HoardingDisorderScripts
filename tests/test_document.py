import pytest
from utils.document import Document
import math


test_files: list[tuple[str, str]] = [
    # First three are chosen from a project that has files from each of 
    # sets 1-3
    ("s1062_s2022-26_s3076-97", "062_745.txt"), 
    ("s1062_s2022-26_s3076-97", "2022_335.txt"), 
    ("s1062_s2022-26_s3076-97", "3001_090.txt"), # Contains a single saying "TRANSCRIPTION PAUSED"
    # Misc files with special cases
    ("s1046-50_s2012-13_s3026-50", "049_606.txt"),
    ("s1_28-35_s2_4-7", "005_083.txt"), # contains "P1: " and "P3: " interview/speaker format
    ("s1_28-35_s2_4-7", "005_082.txt"),
    ("s1_28-35_s2_4-7", "005_086.txt"),
    ("s1036-42_s2008-9_s3000-15", "2008_136.txt"),
    ("s1_21-27_s2_1-3", "026_307.txt"),
]
test_docs = [Document(f"../data/{project}/REVIEW/{filename}.json") 
             for project, filename in test_files]


@pytest.mark.parametrize("row, speaker", [
    # HD Set 1 Tests
    ('Interviewer: ', 'Interviewer'),
    ('Participant: ', 'Participant'),
    ('Rebecca: ', 'Interviewer'),
    ('Interviewee: ', 'Participant'),
    ('Patrick: ', ''),
    (': ', ''),
    (' : ', ''),
    ('Participant 12: ', 'Participant'),
    ('19:24 Interviewer: ', 'Interviewer'),
    ('23:14 Participant: ', 'Participant'),
    ('23:27', ''),
    # HD Sets 2-3 Tests
    ('Interviewer: What is your favorite color?', 'Interviewer'),
    ('Participant: Blue.', 'Participant'),
    ('P1: Okay, kind of inline with that ', 'Interviewer'),
    ('P3: Hm hm, yeah that’s an ', 'Participant'),
])
def test_detect_speaker(row, speaker):
    assert Document._detect_speaker(row) == speaker


@pytest.mark.parametrize("test_doc,expected_speakers", [
    (test_docs[0], [
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
    ]),
    (test_docs[1], ['Interviewer', 'Participant']),
    (test_docs[2], [
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
    ]),
    (test_docs[3], [
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
    ])
])
def test_row_speakers(test_doc, expected_speakers):
    assert test_doc._row_speakers == expected_speakers


@pytest.mark.parametrize("test_doc,expected", [
    (doc, None) for doc in test_docs
])
def test_average_sentence_length(test_doc, expected):
    # If expected is None, just check that the value is a positive float
    asl = test_doc.average_sentence_length
    assert isinstance(asl, float)
    assert asl > 0