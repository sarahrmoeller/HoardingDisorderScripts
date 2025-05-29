from collections import Counter
import json
import re
from itertools import product


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
INTERVIEWER_NAMES = ["Interviewer", "Rebecca"]
PARTICIPANT_NAMES = ["Participant", "Interviewee", "Speaker"]


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
        matches = re.findall(r'([a-zA-z]+(?: \d+)?):', row)
        if any(name in matches for name in INTERVIEWER_NAMES):
            return 'Interviewer'
        elif any(name in matches for name in PARTICIPANT_NAMES):
            return 'Participant'
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
        row_speakers = [''] * len(self.row_data)
        speaker = ""
        for i in range(len(self.row_data)):
            row_data = self.row_data[i][0]
            row_text: str = row_data['content']
            if speaker := self._detect_speaker(row_text):
                row_speakers[i] = speaker
            # If the speaker is not detected, we assume the speaker is the
            # same as the previous row's speaker
            elif i > 0:
                row_speakers[i] = row_speakers[i-1]
            else:
                row_speakers[i] = ''
                raise Warning(f'No speaker found in first row of {self.name}.')
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
            labels_with_speakers[k] = (label_name, speaker)

        return labels_with_speakers

    @property
    def label_counts(self) -> dict[str, str]:
        cntDict = Counter(self.labels)
        for label, speaker in set(
            product(LABELS, ['Interviewer', 'Participant'])
        ).difference(cntDict.keys()):
            cntDict[(label, speaker)] = 0
        cntDict['Total'] = sum(cntDict.values())

        display_dict = {}
        for label in LABELS:
            display_dict[label+'–Interviewer'] = cntDict[(label, 'Interviewer')]
            display_dict[label+'–Participant'] = cntDict[(label, 'Participant')]
            display_dict[label+'–Total'] = cntDict[(label, 'Interviewer')] + \
                                            cntDict[(label, 'Participant')]
        display_dict['Total'] = sum(
            [val for key, val in cntDict.items() if 'Total' in key]
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