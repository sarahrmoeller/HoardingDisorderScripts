from collections import Counter
import json
import re
from itertools import product
import warnings


# List of all labels in the projects
LABELS = {
    'Incomplete Thought',
    'Self Correction',
    'Clarification',
    'Generic Disfluency',
    'Misspeak',
    'Unclear',
    'Overlap'
}
INTERVIEWER_NAMES = ["Interviewer", "Rebecca", "P1"]
PARTICIPANT_NAMES = ["Participant", "Interviewee", "Speaker", "P3"]


class Document:
    """
    Read-only class that provides information relevant to us given a datasaur
    document.
    """
        
    def __init__(self, path: str):
        with open(path) as f:
            raw_data = json.load(f)
        self._raw_data = raw_data['data'] # ignore version number
        self.project = self._raw_data['project']['name']
        self.name = self._raw_data['document']['name']
        self.hoarder_flag = int(self.name[0] == '0')
        # To make it easy to read document properties while debugging
        # Accessing the first element of the row since all rows are singleton
        # lists
        self.row_data = [row[0] for row in self._raw_data['rows']]
        # List of rows in the document indexed by newlines
        self.lines = [ 
            row['content'] for row in self.row_data
        ]
        self.tokens = [token for row in self.row_data for token in row['tokens']]
        # Sentences are decided by splitting on periods
        self.sentences = [
            sent for line in self.lines 
            for sent in line.split('.')
        ]
        self.content = ''.join(self.sentences).replace('\r', '\n')

    @classmethod
    def _detect_speaker(cls, row: str) -> str:
        """
        Expects a datasaur row, and returns whether the speaker is the
        interviewer, 'Interviewer'; the participant, 'Participant'; or unknown,
        in which case the function returns the empty string, ''.
        """
        matches = re.findall(r'([a-zA-z0-9]+)(?: \d+)?:', row)
        if any(name in matches for name in INTERVIEWER_NAMES):
            return 'Interviewer'
        elif any(name in matches for name in PARTICIPANT_NAMES):
            return 'Participant'
        return ''
    
    @classmethod
    def _other_speaker(cls, speaker: str) -> str:
        """
        Expects a speaker, and returns the other speaker.
        If the speaker is 'Interviewer', returns 'Participant'.
        If the speaker is 'Participant', returns 'Interviewer'.
        If the speaker is neither, returns an empty string.
        """
        if speaker in INTERVIEWER_NAMES:
            return PARTICIPANT_NAMES[0]
        if speaker in PARTICIPANT_NAMES:
            return INTERVIEWER_NAMES[0]
        return ''

    @property
    def _row_speakers(self) -> list[str]:
        """
        Expects a list of row data from from the datasaur document.
        Returns a list where index in this list corresponds to a row in the 
        document, and each index in the list contains the speaker of that row.
        This list can be thought of as a mapping between each row index and the
        speaker of the row corresponding to each index.
        """
        row_speakers = [''] * len(self.lines)
        speaker = ""
        first_row_empty = False
        for i in range(len(self.lines)):
            line = self.lines[i]
            speaker = self._detect_speaker(line)
            row_speakers[i] = speaker
            # If no speaker found...
            if not speaker:
                # If not at the first row, assume speaker is the same as previous 
                # speaker (even if no speaker was found in the previous row)
                if i > 0:
                    row_speakers[i] = row_speakers[i-1]
                # If we are at the first row, indicate the first row is empty.
                # Ideally, once we find a row with a speaker, we can fill in all
                # previous rows with the other speaker.
                else:
                    first_row_empty = True
            elif first_row_empty:
                row_speakers[0:i] = [self._other_speaker(speaker)] * i
                first_row_empty = False
        
        rows_without_speakers = tuple(i for i in range(len(row_speakers)) 
                                      if not row_speakers[i])
        if any(rows_without_speakers):
            warnings.warn(
                f'Rows {rows_without_speakers} in document {self.name} '
                f'(Project {self.project}) are missing speakers.'
            )
        return row_speakers

    @property
    def labels(self) -> list[tuple[str, str]]:
        """
        Expects a list of label data from the datasaur document,
        Returns the tuple 
            (label_name, speaker),
        where label is the label's name and speaker is the label's speaker.
        """
        label_data = self._raw_data['spanLabels']
        labels_with_speakers = [('', '')] * len(label_data)

        for k in range(len(label_data)):
            label = label_data[k]

            label_name = label['labelItem']['labelName']
            row_index = label['textPosition']['start']['row']
            speaker = self._row_speakers[row_index] 
            if not speaker:
                warnings.warn(
                    f'No speaker found for {label_name} label in row '
                    f'{row_index} of document {self.name} (Project '
                    f'{self.project}).'
                )
            labels_with_speakers[k] = (label_name, speaker)

        return labels_with_speakers

    @property
    def label_counts(self) -> dict[str, str]:
        cntDict = Counter(self.labels)
        for label, speaker in set(
            product(LABELS, ['Interviewer', 'Participant'])
        ).difference(cntDict.keys()):
            cntDict[(label, speaker)] = 0

        display_dict = {}
        for label in LABELS:
            display_dict[label+'–Interviewer'] = cntDict[(label, 'Interviewer')]
            display_dict[label+'–Participant'] = cntDict[(label, 'Participant')]
            display_dict[label+'–Total'] = cntDict[(label, 'Interviewer')] + \
                                            cntDict[(label, 'Participant')]
        display_dict['Total'] = sum(
            [val for key, val in display_dict.items() if 'Total' in key]
        )

        return display_dict

    @property
    def type_token_ratio(self):
        # Type-token ratio (TTR)
        return len(set(self.tokens)) / len(self.tokens)

    @property
    def average_sentence_length(self, omit_speaker=True):
        # Only omit speaker if the document is a hoarder document due to 
        # single lines/sentences that appear in these sets # that look like 
        # 'Interviewer: ' or 'Participant: ' which are not actual sentences
        if self.hoarder_flag and omit_speaker:
            sents = [
                sent for sent in self.sentences 
                if not self._detect_speaker(sent)
            ]
        else: 
            sents = self.sentences
        return len(self.tokens) / len(sents)