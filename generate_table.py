from collections import Counter
import json
import os
import pandas as pd
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
PARTICIPANT_NAMES = ["Participant", "Interviewee"]

class Document:
    """
    Read-only class that provides information relevant to us given a datasaur
    document.
    """
        
    def __init__(self, path: dict):
        with open(path) as f:
            raw_data = json.load(f)
        self._raw_data = raw_data['data'] # ignore version number
        self.project = self._raw_data['project']['name']
        self.name = self._raw_data['document']['name']
        self.hoarder_flag = int(self.name[0] == '0')
        self.tokens_by_sent = [
            row[0]['tokens'] for row in self._raw_data['rows']
        ]
        self.tokens = [token for row in self.tokens_by_sent for token in row]

        # To make it easy to read the document while debugging
        self.sentences = [row[0]['content'] for row in self._raw_data['rows']]
        self.content = ''.join(self.sentences).replace('\r', '\n')

    @property
    def _row_speakers(self) -> list[str]:
        """
        Expects a list of row data from from the datasaur document.
        Returns a list where index in this list corresponds to a row in the 
        document, and each index in the list contains the speaker of that row.
        """
        rows = self._raw_data['rows']
        row_speakers = [''] * len(rows)
        speaker = ""
        for i in range(len(rows)):
            row = self._raw_data['rows'][i]
            for column in row:
                if (column['content'].find(":") != -1):
                    slice_with_potential_speaker: str = column['content'].split(":")[0].title()
                    speaker_found = False
                    for name in INTERVIEWER_NAMES:
                        if name in slice_with_potential_speaker:
                            speaker = INTERVIEWER_NAMES[0]
                            break
                    # Don't look for participant name if we already found the interviewer
                    if not speaker_found: 
                        for name in PARTICIPANT_NAMES:
                            if name in slice_with_potential_speaker:
                                speaker = PARTICIPANT_NAMES[0]
                                break
                row_speakers[i] = speaker
        return row_speakers


    @property
    def labels(self) -> tuple[str]:
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
    def label_counts(self) -> dict[str]:
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
        display_dict['Total'] = sum(cntDict.values())

        return display_dict

    @property
    def type_token_ratio(self):
        # Type-token ratio (TTR)
        return len(set(self.tokens)) / len(self.tokens)

    @property
    def average_sentence_length(self):
        return len(self.tokens) / len(self.tokens_by_sent)


if __name__ == "__main__":
    table_rows = []
    project_dirs = os.listdir('./data')
    project_dirs.remove('.gitignore')

    for project_dir in project_dirs:
        # Only looking in the REVIEW directory, as this directory contains all
        # adjudicated documents (and not documents with labels from only one 
        # person)
        review_dir = f"./data/{project_dir}/REVIEW/"
        json_files = os.listdir(review_dir)

        project_docs = [Document(review_dir + file) for file in json_files]
        # List of rows in the csv file 
        project_rows = list(map(lambda doc: { 
            'Project' : project_dir,
            'Document Name' : doc.name, 
            'Hoarder Flag' : doc.hoarder_flag,
            **doc.label_counts,
            'TTR' : doc.type_token_ratio,
            'ASL' : doc.average_sentence_length,
        }, project_docs))
        table_rows.extend(project_rows)

    df = pd.DataFrame(table_rows)
    df.to_csv('./out/table.csv', index=False)