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


@pytest.mark.parametrize("test_doc,speaker,speaker_labels,expected_lines", [
    pytest.param(test_docs["062_745.txt"], "Interviewer", True,
                 ["29:19 Interviewer:",
                  "Okay, and what do you think about when you hear the words “hoarding disorder?”",
                  "29:17 Interviewer:",
                  "Okay, so in our last section, I just have a couple more questions for you. Do your problems with clutter upset you?",
                  "30:05 Interviewer:",
                  "Right, so you mentioned that it gets in the way of everything, so would you say it gets in the way of your daily life?",
                  "31:11 Interviewer:",
                  "So could you describe a time where your clutter got in the way of something you really wanted? I know you mentioned that it’s difficult to entertain and have people over because it’s embarrassing to you.",
                  "31:51 Interviewer:",
                  "So definitely it gets in the way of your family time.",
                  "32:07 Interviewer:",
                  "Okay, and has your clutter ever impacted your work?"],
                 id="Set 1 doc, Interviewer lines w/ labels"),
    pytest.param(test_docs["062_745.txt"], "Interviewer", False,
                 ["29:19",
                  "Okay, and what do you think about when you hear the words “hoarding disorder?”",
                  "29:17",
                  "Okay, so in our last section, I just have a couple more questions for you. Do your problems with clutter upset you?",
                  "30:05",
                  "Right, so you mentioned that it gets in the way of everything, so would you say it gets in the way of your daily life?",
                  "31:11",
                  "So could you describe a time where your clutter got in the way of something you really wanted? I know you mentioned that it’s difficult to entertain and have people over because it’s embarrassing to you.",
                  "31:51",
                  "So definitely it gets in the way of your family time.",
                  "32:07",
                  "Okay, and has your clutter ever impacted your work?"],
                 id="Set 1 doc, Interviewer lines no labels"),
    pytest.param(test_docs["062_745.txt"], "Participant", True,
                 ["Participant:",
                  "I think, you know, somebody who has a uh…. Well for a lack of a better term, mental problem, and, you know… I don’t know, because these people are hanging on to things because they can’t get rid of them, and mine is more like I’m too lazy to go through and get rid of stuff. I don’t generally have a problem disposing of things or getting rid of things, unless it’s something that, you know, either has memories or it’s something that I’m collecting. Yeah so, I don’t know if I’m just lazy and don’t want to do it.. I don’t know!",
                  "Participant:",
                  "Yeah. It upsets me, you know, because we can’t really have people in here to have like a dinner party or anything. There’s no room. It upsets my family. It gets in the way of everything, you know, it always pisses my husband off, and he gets pissed off at enough things, you’d think I'd be able to control this to where it’s one less thing he’d be pissed about.",
                  "Participant:",
                  "Not so much, you know, if we vacuum around it, but you know, it’s in the way because the room cannot be used the way it’s supposed to be used. There’s not enough room in it with all the clutter in it on top of things, and it just looks disorganized and messy and, you know, you don’t really want to have visitors or friends come over. I look at other people’s houses and they’re all clean and lovely and lots of space and no problems. And I look at my front room and it's embarrassing! And it looks like I’m, for lack of a better word, trailer trash or something. Yeah it is a better word! My daughter’s here!",
                  "Participant:",
                  "Well more importantly than being embarrassing, the way that I couldn’t house my daughter here the way that would be best for everyone was really impacting the lives of everyone else in this house, so that was a big impact for about a week here.",
                  "Participant:",
                  "And just being an eyesore, you know, the fact that my husband can’t stand it. It’s just all around bad."],
                 id="Set 1 doc with only lines, Participant lines w/ labels"),
    pytest.param(test_docs["062_745.txt"], "Participant", False,
                 ["I think, you know, somebody who has a uh…. Well for a lack of a better term, mental problem, and, you know… I don’t know, because these people are hanging on to things because they can’t get rid of them, and mine is more like I’m too lazy to go through and get rid of stuff. I don’t generally have a problem disposing of things or getting rid of things, unless it’s something that, you know, either has memories or it’s something that I’m collecting. Yeah so, I don’t know if I’m just lazy and don’t want to do it.. I don’t know!",
                  "Yeah. It upsets me, you know, because we can’t really have people in here to have like a dinner party or anything. There’s no room. It upsets my family. It gets in the way of everything, you know, it always pisses my husband off, and he gets pissed off at enough things, you’d think I'd be able to control this to where it’s one less thing he’d be pissed about.",
                  "Not so much, you know, if we vacuum around it, but you know, it’s in the way because the room cannot be used the way it’s supposed to be used. There’s not enough room in it with all the clutter in it on top of things, and it just looks disorganized and messy and, you know, you don’t really want to have visitors or friends come over. I look at other people’s houses and they’re all clean and lovely and lots of space and no problems. And I look at my front room and it's embarrassing! And it looks like I’m, for lack of a better word, trailer trash or something. Yeah it is a better word! My daughter’s here!",
                  "Well more importantly than being embarrassing, the way that I couldn’t house my daughter here the way that would be best for everyone was really impacting the lives of everyone else in this house, so that was a big impact for about a week here.",
                  "And just being an eyesore, you know, the fact that my husband can’t stand it. It’s just all around bad."],
                 id="Set 1 doc with only lines, Participant lines no labels"),
    pytest.param(test_docs["2022_335.txt"], "Interviewer", True,
                 ["Interviewer: Sorry, so the last of the criteria that I'd like to talk through with you is about distress and it's gonna move us into a conversation about insight that you've kind of already foreshadowed, and the criteria reads, \"this difficulty is due to a perceived need to save the items and to distress associated with discarding them.\" And so the question that I have is about how you're determining distress in this context? If a patient has very low insight and doesn't think that their hoarding is a problem, you know, denies that they are at all distressed and says they're perfectly happy with their space the way that it is, how is the distress kind of criteria met or if the person says they're not impaired, how do you determine what constitutes impairment?"],
                 id="Set 2 doc with only two lines, Interviewer lines w/ label"),
    pytest.param(test_docs["2022_335.txt"], "Interviewer", False,
                 ["Sorry, so the last of the criteria that I'd like to talk through with you is about distress and it's gonna move us into a conversation about insight that you've kind of already foreshadowed, and the criteria reads, \"this difficulty is due to a perceived need to save the items and to distress associated with discarding them.\" And so the question that I have is about how you're determining distress in this context? If a patient has very low insight and doesn't think that their hoarding is a problem, you know, denies that they are at all distressed and says they're perfectly happy with their space the way that it is, how is the distress kind of criteria met or if the person says they're not impaired, how do you determine what constitutes impairment?"],
                 id="Set 2 doc with only two lines, Interviewer lines no labels"),
    pytest.param(test_docs["2022_335.txt"], "Participant", True,
                 ["Interviewee: Yeah I think the distress question is slightly more difficult than the impairment question. I think often times it is the collateral context, the people around the person with hoarding that are the distress markers, if you will. So they are the family members or the housing inspector or the child welfare organization, are the markers of distress so they are the ones who are bothered by the saving and the manifestation of the objects, and sometimes in the face of that evidence in clinical interview I have been successful in having clients acknowledge at least why others might be distressed, even if they are not distressed. So they continue to deny their own, but are willing to say, \"yes I hear it from other people and I can see why they would be bothered and/or worried.\" So that's one path that I take in clinical interview for assessment purposes of distress. I think the measures--and I would say that the measures that we have, the standardized measures, you know the hoarding rating scale or the saving inventory revise very little in these ways. They do more in the area of impairment if the person has some amount of insight, but we know that insight of course, or lack thereof, is part of the pathology of this problem. It's also fluctuating, right, so in any given moment a person may be able to say, \"yes this is deeply impairing and deeply distressing\" and in the very next moment they may deny both of those things, again as part of the illness. So I think both, for me clinically, both distress and impairment is part of my clinical interview more than, I come at those things through the clinical interview more than I use those standardized assessments. I don't think what we have available right now does a very good job."],
                 id="Set 2 doc with only two lines, Participant lines w/ label"),
    pytest.param(test_docs["2022_335.txt"], "Participant", False,
                 ["Yeah I think the distress question is slightly more difficult than the impairment question. I think often times it is the collateral context, the people around the person with hoarding that are the distress markers, if you will. So they are the family members or the housing inspector or the child welfare organization, are the markers of distress so they are the ones who are bothered by the saving and the manifestation of the objects, and sometimes in the face of that evidence in clinical interview I have been successful in having clients acknowledge at least why others might be distressed, even if they are not distressed. So they continue to deny their own, but are willing to say, \"yes I hear it from other people and I can see why they would be bothered and/or worried.\" So that's one path that I take in clinical interview for assessment purposes of distress. I think the measures--and I would say that the measures that we have, the standardized measures, you know the hoarding rating scale or the saving inventory revise very little in these ways. They do more in the area of impairment if the person has some amount of insight, but we know that insight of course, or lack thereof, is part of the pathology of this problem. It's also fluctuating, right, so in any given moment a person may be able to say, \"yes this is deeply impairing and deeply distressing\" and in the very next moment they may deny both of those things, again as part of the illness. So I think both, for me clinically, both distress and impairment is part of my clinical interview more than, I come at those things through the clinical interview more than I use those standardized assessments. I don't think what we have available right now does a very good job."],
                 id="Set 2 doc with only two lines, Participant lines"),
])
def test_lines_by_speaker(test_doc, speaker, speaker_labels, expected_lines):
    assert test_doc.lines_by_speaker(speaker, 
                                     speaker_labels=speaker_labels) == expected_lines


@pytest.mark.parametrize("test_doc,speaker,speaker_labels,expected_lines", [
    pytest.param(test_docs["062_745.txt"], "Interviewer", True,
                 "29:19 Interviewer:\n"
                 "Okay, and what do you think about when you hear the words “hoarding disorder?”\n"
                 "29:17 Interviewer:\n"
                 "Okay, so in our last section, I just have a couple more questions for you. Do your problems with clutter upset you?\n"
                 "30:05 Interviewer:\n"
                 "Right, so you mentioned that it gets in the way of everything, so would you say it gets in the way of your daily life?\n"
                 "31:11 Interviewer:\n"
                 "So could you describe a time where your clutter got in the way of something you really wanted? I know you mentioned that it’s difficult to entertain and have people over because it’s embarrassing to you.\n"
                 "31:51 Interviewer:\n"
                 "So definitely it gets in the way of your family time.\n"
                 "32:07 Interviewer:\n"
                 "Okay, and has your clutter ever impacted your work?",
                 id="Set 1 doc, Interviewer lines"),
    pytest.param(test_docs["062_745.txt"], "Interviewer", False,
                 "29:19\n"
                 "Okay, and what do you think about when you hear the words “hoarding disorder?”\n"
                 "29:17\n"
                 "Okay, so in our last section, I just have a couple more questions for you. Do your problems with clutter upset you?\n"
                 "30:05\n"
                 "Right, so you mentioned that it gets in the way of everything, so would you say it gets in the way of your daily life?\n"
                 "31:11\n"
                 "So could you describe a time where your clutter got in the way of something you really wanted? I know you mentioned that it’s difficult to entertain and have people over because it’s embarrassing to you.\n"
                 "31:51\n"
                 "So definitely it gets in the way of your family time.\n"
                 "32:07\n"
                 "Okay, and has your clutter ever impacted your work?",
                 id="Set 1 doc, Interviewer lines"),
    pytest.param(test_docs["062_745.txt"], "Participant", True,
                 "Participant:\n"
                 "I think, you know, somebody who has a uh…. Well for a lack of a better term, mental problem, and, you know… I don’t know, because these people are hanging on to things because they can’t get rid of them, and mine is more like I’m too lazy to go through and get rid of stuff. I don’t generally have a problem disposing of things or getting rid of things, unless it’s something that, you know, either has memories or it’s something that I’m collecting. Yeah so, I don’t know if I’m just lazy and don’t want to do it.. I don’t know!\n"
                 "Participant:\n"
                 "Yeah. It upsets me, you know, because we can’t really have people in here to have like a dinner party or anything. There’s no room. It upsets my family. It gets in the way of everything, you know, it always pisses my husband off, and he gets pissed off at enough things, you’d think I'd be able to control this to where it’s one less thing he’d be pissed about.\n"
                 "Participant:\n"
                 "Not so much, you know, if we vacuum around it, but you know, it’s in the way because the room cannot be used the way it’s supposed to be used. There’s not enough room in it with all the clutter in it on top of things, and it just looks disorganized and messy and, you know, you don’t really want to have visitors or friends come over. I look at other people’s houses and they’re all clean and lovely and lots of space and no problems. And I look at my front room and it's embarrassing! And it looks like I’m, for lack of a better word, trailer trash or something. Yeah it is a better word! My daughter’s here!\n"
                 "Participant:\n"
                 "Well more importantly than being embarrassing, the way that I couldn’t house my daughter here the way that would be best for everyone was really impacting the lives of everyone else in this house, so that was a big impact for about a week here.\n"
                 "Participant:\n"
                 "And just being an eyesore, you know, the fact that my husband can’t stand it. It’s just all around bad.",
                 id="Set 1 doc with only lines, Participant lines"),
    pytest.param(test_docs["062_745.txt"], "Participant", False,
                 "I think, you know, somebody who has a uh…. Well for a lack of a better term, mental problem, and, you know… I don’t know, because these people are hanging on to things because they can’t get rid of them, and mine is more like I’m too lazy to go through and get rid of stuff. I don’t generally have a problem disposing of things or getting rid of things, unless it’s something that, you know, either has memories or it’s something that I’m collecting. Yeah so, I don’t know if I’m just lazy and don’t want to do it.. I don’t know!\n"
                 "Yeah. It upsets me, you know, because we can’t really have people in here to have like a dinner party or anything. There’s no room. It upsets my family. It gets in the way of everything, you know, it always pisses my husband off, and he gets pissed off at enough things, you’d think I'd be able to control this to where it’s one less thing he’d be pissed about.\n"
                 "Not so much, you know, if we vacuum around it, but you know, it’s in the way because the room cannot be used the way it’s supposed to be used. There’s not enough room in it with all the clutter in it on top of things, and it just looks disorganized and messy and, you know, you don’t really want to have visitors or friends come over. I look at other people’s houses and they’re all clean and lovely and lots of space and no problems. And I look at my front room and it's embarrassing! And it looks like I’m, for lack of a better word, trailer trash or something. Yeah it is a better word! My daughter’s here!\n"
                 "Well more importantly than being embarrassing, the way that I couldn’t house my daughter here the way that would be best for everyone was really impacting the lives of everyone else in this house, so that was a big impact for about a week here.\n"
                 "And just being an eyesore, you know, the fact that my husband can’t stand it. It’s just all around bad.",
                 id="Set 1 doc with only lines, Participant lines"),
    pytest.param(test_docs["2022_335.txt"], "Interviewer", True,
                 "Interviewer: Sorry, so the last of the criteria that I'd like to talk through with you is about distress and it's gonna move us into a conversation about insight that you've kind of already foreshadowed, and the criteria reads, \"this difficulty is due to a perceived need to save the items and to distress associated with discarding them.\" And so the question that I have is about how you're determining distress in this context? If a patient has very low insight and doesn't think that their hoarding is a problem, you know, denies that they are at all distressed and says they're perfectly happy with their space the way that it is, how is the distress kind of criteria met or if the person says they're not impaired, how do you determine what constitutes impairment?",
                 id="Set 2 doc with only two lines, Interviewer lines"),
    pytest.param(test_docs["2022_335.txt"], "Interviewer", False,
                 "Sorry, so the last of the criteria that I'd like to talk through with you is about distress and it's gonna move us into a conversation about insight that you've kind of already foreshadowed, and the criteria reads, \"this difficulty is due to a perceived need to save the items and to distress associated with discarding them.\" And so the question that I have is about how you're determining distress in this context? If a patient has very low insight and doesn't think that their hoarding is a problem, you know, denies that they are at all distressed and says they're perfectly happy with their space the way that it is, how is the distress kind of criteria met or if the person says they're not impaired, how do you determine what constitutes impairment?",
                 id="Set 2 doc with only two lines, Interviewer lines"),
    pytest.param(test_docs["2022_335.txt"], "Participant", True,
                 "Interviewee: Yeah I think the distress question is slightly more difficult than the impairment question. I think often times it is the collateral context, the people around the person with hoarding that are the distress markers, if you will. So they are the family members or the housing inspector or the child welfare organization, are the markers of distress so they are the ones who are bothered by the saving and the manifestation of the objects, and sometimes in the face of that evidence in clinical interview I have been successful in having clients acknowledge at least why others might be distressed, even if they are not distressed. So they continue to deny their own, but are willing to say, \"yes I hear it from other people and I can see why they would be bothered and/or worried.\" So that's one path that I take in clinical interview for assessment purposes of distress. I think the measures--and I would say that the measures that we have, the standardized measures, you know the hoarding rating scale or the saving inventory revise very little in these ways. They do more in the area of impairment if the person has some amount of insight, but we know that insight of course, or lack thereof, is part of the pathology of this problem. It's also fluctuating, right, so in any given moment a person may be able to say, \"yes this is deeply impairing and deeply distressing\" and in the very next moment they may deny both of those things, again as part of the illness. So I think both, for me clinically, both distress and impairment is part of my clinical interview more than, I come at those things through the clinical interview more than I use those standardized assessments. I don't think what we have available right now does a very good job.",
                 id="Set 2 doc with only two lines, Participant lines"),
    pytest.param(test_docs["2022_335.txt"], "Participant", False,
                 "Yeah I think the distress question is slightly more difficult than the impairment question. I think often times it is the collateral context, the people around the person with hoarding that are the distress markers, if you will. So they are the family members or the housing inspector or the child welfare organization, are the markers of distress so they are the ones who are bothered by the saving and the manifestation of the objects, and sometimes in the face of that evidence in clinical interview I have been successful in having clients acknowledge at least why others might be distressed, even if they are not distressed. So they continue to deny their own, but are willing to say, \"yes I hear it from other people and I can see why they would be bothered and/or worried.\" So that's one path that I take in clinical interview for assessment purposes of distress. I think the measures--and I would say that the measures that we have, the standardized measures, you know the hoarding rating scale or the saving inventory revise very little in these ways. They do more in the area of impairment if the person has some amount of insight, but we know that insight of course, or lack thereof, is part of the pathology of this problem. It's also fluctuating, right, so in any given moment a person may be able to say, \"yes this is deeply impairing and deeply distressing\" and in the very next moment they may deny both of those things, again as part of the illness. So I think both, for me clinically, both distress and impairment is part of my clinical interview more than, I come at those things through the clinical interview more than I use those standardized assessments. I don't think what we have available right now does a very good job.",
                 id="Set 2 doc with only two lines, Participant lines"),
])
def test_content_by_speaker(test_doc, speaker, speaker_labels, expected_lines):
    assert test_doc.content_by_speaker(speaker, speaker_labels=speaker_labels) == expected_lines