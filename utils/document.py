from collections import Counter
import json
from . import ling
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
# List of Interviewer/Participant speaker name tuples found in the data.
# We commented to the right which set the pair was found in.
# We use the convention that the last speaker in the tuple is the participant,
# and all other speakers are interviewers.
SPEAKER_PAIRS: list[tuple] = [
    ("Interviewer", "Participant"), # Hoarding-Patient
    ("Rebecca", "Interviewee"), # "Hoarding-Clinician" 
    ("Interviewer", "Speaker"), # Parents
    ("P1", "P3", "Interviewee"), # Transcript no. (2)005
    ("P1", "P2", "Interviewee") # Transcript no. 2008
]
SPEAKERS: set = {speaker for pair in SPEAKER_PAIRS for speaker in pair}


class Document:
    """
    Read-only class that provides information relevant to us given a datasaur
    document.
    """

    # Define the default speaker names to use for display in output table
    # Default interviewer name is at index 0, and default participant name is
    # at index 1
    default_speaker_pair = SPEAKER_PAIRS[0]
    # This regex is used to match timestamps, i.e. '19:24' or '23:14'
    _TIMESTAMPS_REGEX = re.compile(r'(\d+:\d+)')
        
    def __init__(self, path: str) -> None:
        with open(path) as f:
            raw_data = json.load(f)
        self._raw_data = raw_data['data'] # ignore version number
        self.project = self._raw_data['project']['name']
        self.name = self._raw_data['document']['name']
        self.transcript_number = self.name.split('_')[0]
        self.hoarder_flag = int(self.name[0] == '0')
        # To make it easy to read document properties while debugging
        # Accessing the first element of the row since all rows are singleton
        # lists
        self.row_data = [row[0] for row in self._raw_data['rows']]
        # List of rows in the document indexed by carriage returns
        self.lines = [
            row['content'].rstrip() for row in self.row_data
        ]
        self.content = '\n'.join(self.lines)
        self.tokens = [token for row in self.row_data for token in row['tokens']]
        # Sentences are decided by splitting on periods
        self.sentences = []
        sent = []
        for token in self.tokens:
            sent.append(token)
            if token.endswith(('.', '!', '?')):  # end of sentence
                self.sentences.append(sent)
                sent = []
        # If there are remaining tokens in the last sentence, add the sentence
        if sent: 
            self.sentences.append(sent)

    def _find_speakers(self, content: str) -> list[str]:
        """
        Uses re.findall to look for all occurences of valid speaker names 
        (defined in SPEAKERS set) followed by an optional number and mandatory
        colon (i.e. 'Interviewer:' or 'Participant 12: ') in a string. More 
        generally, this finds all parts of a string that look like 
            {speaker_name} [optional number]:
        and returns speaker_name within the `findall` list.
        """
        return re.findall(r'({speaker_names})(?: \d+)?:'
                           .format(speaker_names='|'.join(SPEAKERS)), content)
    
    @property
    def _speaker_set(self) -> set[str]:
        """
        Returns the set of all speakers in the document.
        """
        speaker_matches = self._find_speakers(self.content)
        returned_set = set(speaker_matches)
        if (num_speakers := len(returned_set)) not in (2, 3):
            warnings.warn(
                f'{num_speakers} total speakers found in {self.name} '
                f'({self.project}). Speakers: {returned_set}'
            )
        return returned_set
    
    @property
    def speaker_pair(self) -> tuple:
        """
        Uses the _speaker_set property and SPEAKER_PAIRS to return a tuple of 
        the two speakers in the document, with interviewer indexed at 0 and 
        participant indexed at 1.
        """
        num_speakers = len(self._speaker_set)
        if num_speakers == 0:
            raise ValueError(f'No speakers found in {self.name} '
                             f'({self.project}). Assuming something is wrong.')
        elif num_speakers == 1:
            speaker = next(iter(self._speaker_set))
            return tuple(speaker)
        # If all elements in some speaker pair are in the speaker set, we 
        # assume we've found the right pair
        for pair in SPEAKER_PAIRS:
            if all(speaker in self._speaker_set for speaker in pair):
                return pair
        # If we still haven't found a match, something has gone wrong
        raise ValueError(f'No valid speaker pair found for {self.name} '
                         f'({self.project}). Speakers: {self._speaker_set}')

    @property
    def _row_speakers(self) -> list[str | None]:
        """
        Returns a list where index in this list corresponds to a row in the 
        document, and each index in the list contains the speaker of that row.
        This list can be thought of as a mapping between each row index and the
        speaker of the row corresponding to each index.
        """
        row_speakers: list[str | None] = [None] * len(self.lines)
        current_speaker: str | None = None
        first_row_empty = False
        for i in range(len(self.lines)):
            line = self.lines[i]
            speaker_matches = self._find_speakers(line)
            # If speaker found, change global current_speaker variable
            if speaker_matches:
                # Check: a single line should only have one speaker.
                # If multiple speakers found, warn and use the first one
                if len(speaker_matches) > 1:
                    warnings.warn(
                        f'Multiple speakers found in row {i} of document '
                        f'{self.name} (Project {self.project}). Speakers: '
                        f'{speaker_matches}. Using first speaker.'
                    )
                # TODO: Warn if speaker is found not at the beginning of the 
                # line, ignoring timestamps
                current_speaker = speaker_matches[0]
            row_speakers[i] = current_speaker
            # TODO: Below logic is superfluous
            # If no speaker found...
            if not current_speaker:
                # If not at the first row, assume speaker is the same as previous 
                # speaker (even if no speaker was found in the previous row)
                if i > 0:
                    row_speakers[i] = row_speakers[i-1]
                # If we are at the first row, indicate the first row is empty.
                # Ideally, once we find a row with a speaker, we can fill in all
                # previous rows with the other speaker.
                else:
                    first_row_empty = True
            elif first_row_empty and len(self.speaker_pair) == 2:
                # The "other speaker" is only defined if there are two speakers
                other_speaker = self.speaker_pair[self.speaker_pair
                                                  .index(current_speaker)-1]
                row_speakers[0:i] = [other_speaker] * i
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
    def _row_speakers_default(self) -> list[str]:
        """
        Convert all names in _row_speakers to their default pair names given
        by SPEAKER_PAIRS[0].
        """
        # See default_speaker_pair definition for convention
        default_interviewer_name = Document.default_speaker_pair[0]
        default_participant_name = Document.default_speaker_pair[1]
        last_speaker_in_pair = self.speaker_pair[-1]
        return [default_participant_name if speaker == last_speaker_in_pair 
                else default_interviewer_name 
                for speaker in self._row_speakers]

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
            speaker = self._row_speakers_default[row_index] 
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
            product(LABELS, Document.default_speaker_pair)
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
        """
        Returns the type-token ratio of the document's tokens.
        """
        tokens = [
            token for token in self.tokens 
            if not self._find_speakers(token)
        ]
        return ling.type_token_ratio(tokens)

    @staticmethod
    def valid_sentence(sent: list[str]) -> bool:
        ...

    @property
    def average_sentence_length(self):
        """
        Returns the average number of tokens in each sentence in the document.
        """
        # If a sentence has two or fewer tokens and contains a speaker,
        # we skip the sentence, assuming the sentence looks like 'Interviewer: '
        # or 'Participant: '.
        # Otherwise, we skip the token containing the speaker.
        sents = []
        for sent in self.sentences:
            valid_sent = []
            for token in sent:
                if self._find_speakers(token):
                    if len(sent) <= 2:
                        # skip sentence
                        valid_sent = []
                        break
                    else: 
                        # skip token
                        continue 
                valid_sent.append(token)
            sents.append(valid_sent)
        return ling.average_sentence_length(sents)

    def __str__(self) -> str:
        return f'Document(name=\"{self.name}\", project=\"{self.project}\")'
    
    def __repr__(self) -> str:
        return f'Document(name=\"{self.name}\", project=\"{self.project}\")'