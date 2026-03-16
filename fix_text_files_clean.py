import os
import re

TEXT_FILE_DIRECTORY = './data/mathews/documents/text_files/'

interviewer_errors = [': Interviewer:', 'Interview-', 'interviewer:']

speaker_errors = ['-Speaker:', 'Speaker 1 -', 'Speaker1:', 'Speaker:', 'Participant:']
participant_errors = 'Participant '

note_taker_errors = ['Note Taker-', 'Note taker:']

location_errors = [' UF', ' LOCATION', ' THE_[LOCATION]']
    #Kept [' Bay Area', ' Silicon Valley', ' Mountain View', ' San Francisco'] for now since included in multiple interviews

#Found in 1001 files that were added later
anonymous_errors = ['Lifelock', 'Symantec', 'Broadcom']
age_error1 = ["I'm 66"]
age_error2 = ["birthday in May"]

notes_not_speech = ['[laughter]', '[LAUGHTER]', ' LAUGH', '[LAUGH]', ' LAUGHS', '[LAUGHS]', 'LAUGHING', '[LAUGHING]', 'AFFIRMATIVE', '[affirmative]', '[AFFIRMATIVE]', ' NEGATIVE', '[negative]', '[NEGATIVE]', 'Transcribed by Aqueena', 'Transcripted by Aqueena']

unclear_notes = [' [unclear]', ' UNCLEAR']
inaudible_notes = [' [inaudible]', ' INAUDIBLE']
incoherent_notes = [' [incoherent', ' INCOHERENT']
crosstalk_notes = [' [crosstalk]', ' CROSSTALK']
talking_notes = [' [Talking to person not on the phone]', ' TALKING TO PERSON NOT ON THE PHONE']

paused_notes = ['TRANSCRIPTION PAUSED', 'Transcription Paused – Kendall', 'Transcription paused by Aqueena @', '[CUTS_OUT]']
end_notes = ['END_OF_RECORDING']
end_note_corrections = ['-End of transcript-', 'End of transcription.', 'End of transcription']

underscore = r'__+'

for root, dirs, files in os.walk(f'{TEXT_FILE_DIRECTORY}'):
    for text_file in files:
        if text_file.endswith(".txt"):
            file_path = os.path.join(root, text_file)
            with open(file_path, "r") as f:
                clean = f.read()

            """
            Fix interviewer misspellings.
                : Interviewer:  ; [('3001_076.txt', 12)]
                Interview-  ; [('3001_037.txt', 1)]
                interviewer  ; [('3001_030.txt', 8)
                --> Interviewer:
            """
            for error in interviewer_errors:
                clean = clean.replace(f'{error}', 'Interviewer:')

            """
            Interviewee errors. 
            Note: Speaker1 is the same as Speaker in the interviewers.
                -Speaker:  ; [('3001_017.txt', 38)]
                Speaker 1 -  ; [('1058_712.txt', 21)]
                Speaker1:  ; [('3001_011.txt', 58), ('3001_012.txt', 1)]
                Speaker: (set 3)
                Participant: 
                Participant ##: → Interviewee##:        #most consistent with previous changes
                    #'Participant,' used in a sentence file 1052_642
            Changed to 'Interviewee:' in sets 1-3
            """
            for error in speaker_errors:
                clean = clean.replace(f'{error}', 'Interviewee:')
                clean = clean.replace(f'{participant_errors}', 'Interviewee')

            """
            Note Taker in set03. Changed to Interviewer2. However, Interviewer was not changed to Interviewer1 in these files.
            'Note Taker-', 'Note taker:'
            """
            for error in note_taker_errors:
                clean = clean.replace(f'{error}', 'Interviewer2:')

            """
            Location errors
                UF --> [LOCATION]
                ' LOCATION' --> ' [LOCATION]'
                THE_[LOCATION] error in 3001_074.
                1001 files had very specific California information replaced with [LOCATION], and companies, age, and birthday that were replaced with [ANONYMIZATION]
            """
            for error in location_errors:
                clean = clean.replace(f'{error}', ' [LOCATION]')
            for error in anonymous_errors:
                clean = clean.replace(f'{error}', '[ANONYMIZATION]')
            for error in age_error1:
                clean = clean.replace(f'{error}', "I'm [ANONYMIZATION]")
            for error in age_error2:
                clean = clean.replace(f'{error}', "birthday in [ANONYMIZATION]")

            """
            Removing transcriber notes that do not stand in for speech.
            [laughter], [LAUGHTER], LAUGH, [LAUGH], [affirmative], [AFFIRMATIVE], [negative], [NEGATIVE]
            """
            for error in notes_not_speech:
                clean = clean.replace(f'{error}', '')

            """
            Correct transcriber notes that do stand in for speech. Should be in all caps and within brackets.
            [unclear], [inaudible], [incoherent], unclear, [crosstalk], [Talking to person not on the phone], 'END_OF_RECORDING '
            """
            for error in unclear_notes:
                clean = clean.replace(f'{error}', ' [UNCLEAR]')
            for error in inaudible_notes:
                clean = clean.replace(f'{error}', ' [INAUDIBLE]')
            for error in incoherent_notes:
                clean = clean.replace(f'{error}', ' [INCOHERENT]')
            for error in crosstalk_notes:
                clean = clean.replace(f'{error}', ' [CROSSTALK]')
            for error in talking_notes:
                clean = clean.replace(f'{error}', ' [TALKING TO PERSON NOT ON THE PHONE]')

            """
            Transcriptions paused corrections. Should be [PAUSED] or [END_OF_RECORDING]
            """
            for error in paused_notes:
                clean = clean.replace(f'{error}', '[PAUSED]')
            for error in end_notes:
                clean = clean.replace(f'{error}', '[END_OF_RECORDING]')
            for error in end_note_corrections:
                clean = clean.replace(f'{error}', '[END_OF_TRANSCRIPT]')
                #could be removed completely ''
            clean = clean.replace('[[END_OF_RECORDING]]', '[END_OR_RECORDING]')

            """
            Other errors and typos.
                Either/ in 3001_096
                []  in 3001_011     #It is just an empty bracket set
            """
            clean = clean.replace('Either/', 'Either')
            clean = clean.replace('[]', '')

            """
            The underscores. No clear reasoning. 
            Changed to [UNDERSCORES]
            Usually, two underscores next to each other '__', but up to five.
            Single '_' underscores left because some are necessary.
            May stand in for [INAUDIBLE].
            """
            clean = re.sub(underscore, '[UNDERSCORE]', clean)

            with open(file_path, "w") as f:
                f.write(clean)

"""
Dashes left in. Appear as '-' or '--' at the end of the line.
"""

"""
Labeled [TALKING TO PERSON NOT ON THE PHONE] added to files 85 and 87 in set03 manually.
"""

"""
Deleted (manually) duplicated interview Line 17, 047 - Line 35, 053 of set03.
Same interview as Line 5, 029 - Line 21, 035.
"""

"""
Findall function and location.
Check_tokens_initial_list check for all the errors listed in Slack and Github.
Check_tokens is what actually exists in Github and needs to be changed.
Returns which errors still exist in Github for more efficient replacement.
"""

check_tokens_initial_list = ['Speaker 1 -', 'Speaker1:', 'Interiew-', 'Speaker1 -', 'Note Taker-', 'Interviewer1:',
                '-Transcripted by Aqueena', 'Transcription Paused – Kendall', '-Transcribed by Aqueena',
                ': Interviewer:', 'TRANSCRIPTION PAUSED', 'Either/', 'LAUGHS', 'LAUGH', 'LOCATION', '[]',
                'Speaker:', 'Speaker1:', 'Note taker:', '-Speaker:', 'WACKY PEOPLE', 'UF', 'Transcription paused by Aqueena @',
                'interviewer:', 'Interview-', 'Speaker1 -', 'LAUGHTER', 'Note Taker-', 'Interviewer1:', '[problem ##:##:##]', '[agents ##:##:##]',
                '[Sand ##:##:##]', '[Vise by 16 Box in Wrench ##:##:##]', '[Ann ##:##:##]', '[inaudible; (##:##)].',
                '[name of state; (##:##)].', '[talking to someone not on the phone]', '[Talking to person not on the phone]',
                '[unclear]', '[STATE]', '[State]', '[state]', '[PHONE CALL HANGS UP]', '[listing ##:##:##]', '[Lauren Mellin ##:##:##]',
                '[names of companies; ((##:##)]', '[name]', '[Buttonheim ##:##:##]', '[name of place]',
                'Interviewer (34:4y):', '[Laughing]', '[laughing]', '[name of fast food restaurant; (45:15)]',
                'Participant ### (#:##):', 'Participant ### ##:##', 'Participant ### ##:##-', '[unclear]',
                '[location]', 'Speaker # ##:##-', 'Interviewer ##: ##-', 'Interviewer #:##-', '#:## Interviewer:',
                '[unclear] (#:##)', '[unclear](#:##)', '[unclear] (##:##).', '[unclear.]', '##:## Interviewer #:',
                '#Participant:', 'even ##:##:##]', '[virtually ##:##:##]', 'PART 4 of 4 ENDS [01:30:56]',
                '[Josha ##:##:##]', 'Interviewer (#:##):', 'Interviewer (##:##):', 'Participant:', '[Inaudible.]',
                '[inaudible; (##:##)]', '[inaudible]', '[Inaudible]', '[Colleague name]’s', '[Personal demographic info…]',
                '##:## Interviewer:', '[##:##] INCOHERENT', '[imaudible].', '(affirmative)', '[crosstalk ##:##:##]',
                'Participant ###:', '[inaudible ##:##:##]', '[inaudible ##:##:##:##].', '005', '007', '[hell ##:##:##]',
                '[Len 00:12:58]', 'PART 2 of 4 ENDS [00:46:04]', 'PART 3 of 4 ENDS [01:09:04]', '[Currator ##:##:##]',
                '[drawers ##:##:##]', '[waste ##:##:##]', '(negative)', '[relevantly ##:##:##]', '[guess ##:##:##]',
                '(silence)', '[even ##:##:##]', '[virtually ##:##:##]', 'PART 4 of 4 ENDS [01:30:56]', '[Josha ##:##:##]',
                'Interviewer (#:##):', 'Interviewer (##:##):', 'Participant:', '[Inaudible.]', '[inaudible; (##:##)]',
                '[inaudible]', '[Colleague name]’s', '[Personal demographic info…]', '##:## Interviewer:', '[##:##] INCOHERENT',
                '[imaudible].', '[name of place; inaudible; (34:15)]', '“[name of place].”', 'Interviewer (34:4y):',
                '[Laughing]', '[laughing]', '[name of fast food restaurant; (45:15)]', 'Participant ### (#:##):',
                'Participant ### ##:##', 'Participant ### ##:##-', '[unclear]', '[location]', 'Speaker # ##:##-',
                'Interviewer ##: ##-', 'Interviewer #:##-', '#:## Interviewer:', '[unclear] (#:##)', 'unclear',
                '[unclear] (##:##).', '[unclear.]', '##:## Interviewer #:', '#Participant:', '[problem ##:##:##]',
                '[agents ##:##:##]', '[Sand ##:##:##]', '[Vise by 16 Box in Wrench ##:##:##]', '[Ann ##:##:##]',
                '[inaudible; (##:##)].', '[name of state; (##:##)].', '[talking to someone not on the phone]',
                '[Talking to person not on the phone]', '[unclear]', '[STATE]', '[State]', '[state]',
                '[PHONE CALL HANGS UP]', '[listing ##:##:##]', '[Lauren Mellin ##:##:##]', '[names of companies; ((##:##)]',
                '[name]', '[Buttonheim ##:##:##]', 'Participant:', 'Participant #:', 'Participant ###:']

check_tokens = ['-Speaker:', 'Transcribed by Aqueena', 'Transcripted by Aqueena', ': Interviewer:', 'Either/', 'Interview-', ' LAUGH ', ' LAUGHS ', '[LAUGH', ' LOCATION ', 'Note Taker-', 'Note taker:', 'Participant ', 'Participant 34', 'Speaker 1 -', 'Speaker1:', 'Speaker:', 'TRANSCRIPTION PAUSED', 'Transcription Paused – Kendall', 'Transcription paused by Aqueena @', ' UF ', '[]', 'interviewer:', '[unclear]', ' UNCLEAR ']

underscores = ['__', '___', '____', '______']
    #some single underscores, but maybe necessary

found = dict()
regex_happy_list = map(re.escape, check_tokens)
tokens = re.compile("|".join(regex_happy_list))

for root, dirs, files in os.walk(f'{TEXT_FILE_DIRECTORY}'):
    for text_file in files:
        if text_file.endswith(".txt"):
            file_path = os.path.join(root, text_file)
            with open(file_path, "r") as f:
                for line_num, line in enumerate(f, start=1):
                    for match in tokens.finditer(line):
                        key = match.group()
                        if key not in found:
                            found[key] = []
                        found[key].append((file_path[42:], line_num))
for key in sorted(found):
    print(f'{key}  ; {found[key]}')