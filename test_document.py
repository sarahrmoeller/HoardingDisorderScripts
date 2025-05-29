import pytest
from utils.document import Document


test_files: list[tuple[str, str]] = [
    # First three are chosen from a project that has files from each of 
    # sets 1-3
    ("s1062_s2022-26_s3076-97", "062_745.txt"), 
    ("s1062_s2022-26_s3076-97", "2022_335.txt"), 
    ("s1062_s2022-26_s3076-97", "3001_090.txt"), # Contains a single saying "TRANSCRIPTION PAUSED"
    # Misc files with special cases
    ("s1046-50_s2012-13_s3026-50", "049_606.txt"),
    ("s1_28-35_s2_4-7", "005_083.txt")
]
test_docs = [Document(f"./data/{project}/REVIEW/{filename}.json") 
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