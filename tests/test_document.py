import pytest
from utils.document import DatasaurDocument
import json
import os


test_files: list[tuple[str, str]] = [
    # First three are chosen from a project that has files from each of 
    # sets 1-3
    ("s1062_s2022-26_s3076-97-NDQ2OTMwYjg", "062_745"), 
    ("s1062_s2022-26_s3076-97-NDQ2OTMwYjg", "2022_335"), 
    ("s1062_s2022-26_s3076-97-NDQ2OTMwYjg", "3001_090"), # Contains a single line saying "[TRANSCRIPTION PAUSED]"
    # Misc files with special cases
    # ("s1043-5_s2010-11_s3016-25-NjFlYmM5MGE", "049_606"), # Has speaker label with a number, "Participant 49:"
    # ("s1036-42_s2008-9_s3000-15", "2008_118"), # Starts with Interview 008
    ("s1_28-35_s2_4-7-M2Y5YjVkMjM", "2005_083"), # contains "P1: " and "P3: " interview/speaker format
    ("s1_28-35_s2_4-7-M2Y5YjVkMjM", "2005_082"),
    ("s1_28-35_s2_4-7-M2Y5YjVkMjM", "2005_086"),
    # ("s1036-42_s2008-9_s3000-15", "2008_136"),
    ("s1_21-27_s2_1-3-NTE3MmUyODM", "026_307"), # Contains only Interviewer label, as well as [END OF RECORDING]
    ("s1051-54_s2014-19_s3051-75-MDFjZTBkZDY", "051_628"), # Very normal doc that came out as empty for some reason
]
test_docs = {filename: DatasaurDocument(f"./data/mathews/documents/"
                                         "datasaur_exports/truncated_clauses/"
                                        f"{project}/REVIEW/{filename}.json")
             for project, filename in test_files}


@pytest.mark.parametrize("test_doc,expected_speaker_set", [
    pytest.param(test_docs["062_745"], {'Interviewer', 'Participant'}, 
                 id="Test arbitrary set 1 doc"),
    pytest.param(test_docs["2022_335"], {'Interviewer', 'Interviewee'}, 
                 id="Test arbitrary set 2 doc"),
    pytest.param(test_docs["3001_090"], {'Interviewer', 'Speaker'}, 
                 id="Test arbitrary set 3 doc"),
    # pytest.param(test_docs["049_606"], {'Interviewer', 'Participant'}, 
    #              id="Document that doesn't begin with a speaker label"),
    # Do this test after 005 documents are fixed
    pytest.param(test_docs["2005_086"], {'Interviewee', 'P1', 'P3'}, 
                 id="Three-speaker document (Interviewers: P1 and P3)"),
    # pytest.param(test_docs["2008_136"], {'P2', 'Interviewee', 'P1'}, 
    #              id="Three-speaker document (Interviewers: P1 and P2)"),
    pytest.param(test_docs["026_307"], {'Interviewer'}, 
                 id="Contains only Interviewer label, as well as [END OF RECORDING]"), # 
])
def test_speaker_set(test_doc, expected_speaker_set):
    assert test_doc.speaker_set(restrict=True) == expected_speaker_set


@pytest.mark.parametrize("test_doc,expected_speakers", [
    pytest.param(test_docs["062_745"], [ 
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
    pytest.param(test_docs["2022_335"], ['Interviewer', 'Interviewee'], 
                 id="Test arbitrary set 2 doc"),
    pytest.param(test_docs["3001_090"], [
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
    # pytest.param(test_docs["049_606"], [
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant',
    #     'Interviewer', 'Interviewer', 'Interviewer', 'Interviewer', 
    #     'Interviewer',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant'
    # ], id="Document that doesn't begin with a speaker label"),
    (test_docs["2005_086"], [ 
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
    # pytest.param(test_docs["2008_136"], [
    #     'P2',
    #     'Interviewee',
    #     'Interviewee',
    #     'P1',
    #     'Interviewee',
    #     'P2',
    #     'Interviewee',
    #     'P2',
    #     'Interviewee',
    #     'P2',
    #     'Interviewee',
    #     'P2',
    #     'Interviewee'
    # ], id="Three-speaker document"),
    pytest.param(test_docs["026_307"], [
        'Interviewer',
        'Interviewer',
        'Interviewer',
        'Interviewer',
    ], id="Contains only Interviewer label, as well as [END OF RECORDING]"), # 
    pytest.param(test_docs["051_628"], [
        # Lines 1-14 part. of interview
        "Participant", "Participant", "Participant", "Participant",
        "Participant", "Participant", "Participant", "Participant",
        "Participant", "Participant", "Participant", "Participant",
        "Participant", "Participant",
        "Interviewer", "Interviewer", "Interviewer", "Interviewer", # Lines 15-18
        "Participant", "Participant", "Participant", # 19-21
        "Interviewer", "Interviewer", # 22-23
        "Participant", "Participant", # 24-25
        "Interviewer", "Interviewer", "Interviewer", # 26-28
        "Participant", "Participant", # 24-25
        "Interviewer", "Interviewer", # 22-23
    ], id="Very normal doc that should work but didn't"), # 
])
def test_row_speakers(test_doc, expected_speakers):
    assert test_doc._row_speakers == expected_speakers


# Each of these tests are basically the same as the previous one, but
# with all interviewer names changed to 'Interviewer' and all participant names
# changed to 'Participant'. This is useful for testing the default speaker 
@pytest.mark.parametrize("test_doc,expected_speakers", [
    pytest.param(test_docs["062_745"], [
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
    pytest.param(test_docs["2022_335"], ['Interviewer', 'Participant'],
                 id="Test arbitrary set 2 doc with default speakers"),
    pytest.param(test_docs["3001_090"], [
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
    # pytest.param(test_docs["049_606"], [
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant',
    #     'Interviewer', 'Interviewer', 'Interviewer', 'Interviewer', 
    #     'Interviewer',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant',
    #     'Participant', 'Participant', 'Participant', 'Participant'
    # ], id="Document that doesn't begin with a speaker label"),
    (test_docs["2005_086"], [ 
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
    # pytest.param(test_docs["2008_136"], [
    #     'Interviewer',
    #     'Participant',
    #     'Participant',
    #     'Interviewer',
    #     'Participant',
    #     'Interviewer',
    #     'Participant',
    #     'Interviewer',
    #     'Participant',
    #     'Interviewer',
    #     'Participant',
    #     'Interviewer',
    #     'Participant'
    # ], id="Three-speaker document"),
    pytest.param(test_docs["026_307"], [
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