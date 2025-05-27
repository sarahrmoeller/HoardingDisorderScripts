import pytest
from utils.docment import Document


# Using this project directory for testing since it has files from sets 1-3
project_dir = "s1062_s2022-26_s3076-97"
# All files we care about are in the REVIEW directory
review_dir = f"./data/{project_dir}/REVIEW/" 
# One test file from each set
test_files = ["062_745.txt", "2022_335.txt", "3001_090.txt"]
test_docs = [Document(review_dir + filename + '.json') 
             for filename in test_files]


@pytest.mark.parametrize("row, speaker", [
    # HD Set 1 Tests
    ('Interviewer: ', 'Interviewer'),
    ('Participant: ', 'Participant'),
    ('Rebecca: ', 'Interviewer'),
    ('Interviewee: ', 'Participant'),
    ('Patrick: ', ''),
    (': ', ''),
    (' : ', ''),
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
])
def test_row_speakers(test_doc, expected_speakers):
    assert test_doc._row_speakers == expected_speakers