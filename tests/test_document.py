import pytest
from utils.document import Document
import json
import os


test_files: list[tuple[str, str]] = [
    # First three are chosen from a project that has files from each of 
    # sets 1-3
    ("s1062_s2022-26_s3076-97", "062_745.txt"), 
    ("s1062_s2022-26_s3076-97", "2022_335.txt"), 
    ("s1062_s2022-26_s3076-97", "3001_090.txt"), # Contains a single line saying "[TRANSCRIPTION PAUSED]"
    # Misc files with special cases
    ("s1043-5_s2010-11_s3016-25", "049_606.txt"), # Has speaker label with a number, "Participant 49:"
    ("s1036-42_s2008-9_s3000-15", "2008_118.txt"), # Starts with Interview 008
    ("s1_28-35_s2_4-7", "2005_083.txt"), # contains "P1: " and "P3: " interview/speaker format
    ("s1_28-35_s2_4-7", "2005_082.txt"),
    ("s1_28-35_s2_4-7", "2005_086.txt"),
    ("s1036-42_s2008-9_s3000-15", "2008_136.txt"),
    ("s1_21-27_s2_1-3", "026_307.txt"), # Contains only Interviewer label, as well as [END OF RECORDING]
]
test_docs = {filename: Document(f"./data/{project}/REVIEW/{filename}.json")
             for project, filename in test_files}


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
    pytest.param(test_docs["2005_086.txt"], {'Interviewee', 'P1', 'P3'}, 
                 id="Three-speaker document (Interviewers: P1 and P3)"),
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
    (test_docs["2005_086.txt"], [ 
        'P3',
        'P1',
        'P3',
        'P1',
        'Interviewee',
        'P3',
        'Interviewee',
        'P3',
        'Interviewee',
    ]),
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
    (test_docs["2005_086.txt"], [ 
        'Interviewer',
        'Interviewer',
        'Interviewer',
        'Interviewer',
        'Participant',
        'Interviewer',
        'Participant',
        'Interviewer',
        'Participant',
    ]),
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


TEST_DATA_DIR = "./tests/doc_test_data/"

def load_test_data(filename: str) -> dict:
    with open(TEST_DATA_DIR + filename, 'r', 
              encoding='utf-8') as f:
        return json.load(f)


@pytest.mark.parametrize("test_doc,speaker,speaker_labels,cleaned,"
                         "expected_lines", [
    pytest.param(test_docs[filename.rstrip('.json')], 
                 speaker,
                 variant == "raw", # Only enable speaker_labels option if testing raw
                 variant == "cleaned", # Only enable cleaned option if testing cleaned
                 file_data[speaker][variant]["lines"],
                 id=f"{filename} + {speaker} + {variant} + {file_data['id']}")
    for filename in os.listdir(TEST_DATA_DIR) 
    for speaker in ("Interviewer", "Participant")
    for variant in ("raw", "no-speaker-labels", "cleaned")
    if filename.endswith(".json") and 
    speaker in (file_data := load_test_data(filename)) and 
    variant in file_data[speaker].keys()
])
def test_lines_by_speaker(test_doc, speaker, speaker_labels, cleaned, 
                          expected_lines):
    assert test_doc.lines_by_speaker(speaker, 
                                     speaker_labels=speaker_labels,
                                     cleaned=cleaned) == expected_lines


@pytest.mark.parametrize("test_doc,speaker,speaker_labels,cleaned," \
                         "expected_lines", [
    pytest.param(test_docs[filename.rstrip('.json')], 
                 speaker,
                 variant == "raw",
                 variant == "cleaned",
                 file_data[speaker][variant]["content"],
                 id=f"{filename} + {speaker} + {variant} + {file_data['id']}")
    for filename in os.listdir(TEST_DATA_DIR) 
    for speaker in ("Interviewer", "Participant")
    for variant in ("raw", "no-speaker-labels", "cleaned")
    if filename.endswith(".json") and 
    speaker in (file_data := load_test_data(filename)) and 
    variant in file_data[speaker].keys() and
    'content' in file_data[speaker][variant].keys()
])
def test_content_by_speaker(test_doc, speaker, speaker_labels, cleaned, 
                            expected_lines):
    assert test_doc.content_by_speaker(speaker, 
                                       speaker_labels=speaker_labels,
                                       cleaned=cleaned) == expected_lines