from collections import Counter
from functools import cached_property
from itertools import product
import json
from . import ling
import re
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
    ("Interviewer", "Speaker"), # Parents
    ("Interviewer", "Interviewee"), # Transcript no. 012 & 2010
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
    # This regex is used to match speaker labels, i.e. 'Interviewer:', 'Participant 12:'
    _SPEAKER_REGEX = re.compile(r'([a-zA-Z][a-zA-Z0-9]+)(?:\s+\d+)?:')
    # This regex is used to match timestamps, i.e. '19:24' or '23:14'
    _TIMESTAMPS_REGEX = re.compile(r'(\d+:\d+)')
        
    def __init__(self, path: str) -> None:
        with open(path) as f:
            self.json_dump = json.load(f)
        # JSON always looks like {'version' : '1.0', 'data' : {...}},
        # So we will just index into the 'data' key
        self.data = self.json_dump['data']
        self.project = self.data['project']['name']
        self.name = self.data['document']['name']
        self.transcript_number = self.name.split('_')[0]
        self.set = 1 if self.name[0] == '0' else int(self.name[0])
        assert self.set in (1, 2, 3)
        self.hoarder_flag = int(self.set == 1)
        # To make it easy to read document properties while debugging
        # Accessing the first element of the row since all rows are singleton
        # lists
        self.row_data: list[dict] = [row[0] for row in self.data['rows']]
        # List of rows in the document indexed by carriage returns
        self.lines = [
            row['content'].rstrip() for row in self.row_data
        ]
        self.content = '\n'.join(self.lines)
        self.tokens = [token for row in self.row_data for token in row['tokens']]
        # Sentences are decided by splitting on periods
        self.label_data = self.data['spanLabels']
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

    @classmethod
    def find_speakers(cls, content: str, restrict=True) -> list[str]:
        """
        Takes in a string (`content`),
        Returns a list of all occurences of strings followed by optional whitespace, 
        optional number(s), and a colon. It then captures the string. Format:
            (captured string) [optional number]:
        If `restrict` is True, it only returns speakers that are in the `SPEAKERS` set.

        Examples: 
        - 'Interviewer:' -> ['Interviewer']
        - 'Participant 12: ' -> ['Participant 12']
        - 'Spongebob:' -> [] (if `restrict` is True, since 'Spongebob' is not in `SPEAKERS`)
        """
        matches = Document._SPEAKER_REGEX.findall(content)
        if not restrict:
            return matches
        return [match for match in matches if match in SPEAKERS]
    
    def speaker_set(self, restrict=True) -> set[str]:
        """
        Returns the set of all speaker labels found in the document.
        """
        speaker_matches = self.find_speakers(self.content, restrict=restrict)
        if not speaker_matches:
            # There should never be 0 speakers in a document
            raise ValueError(f'No speakers found in {self}. '
                             f'Assuming something is wrong.')
        return set(speaker_matches)
    
    @cached_property
    def speaker_tuple(self) -> tuple:
        """
        Uses the _speaker_set property to find which pair of speakers in 
        SPEAKER_PAIRS is speaking in the document.
        """
        if len(self.speaker_set()) == 1:
            # If we only find one speaker label, find the pair in 
            # SPEAKER_PAIRS that contains that label
            speaker = next(iter(self.speaker_set()))
            pairs_with_speaker = [pair for pair in SPEAKER_PAIRS 
                                  if speaker in pair]
            # If we find more than one pair, give up.
            if len(pairs_with_speaker) > 1:
                warnings.warn(f'Not enough information to determine '
                               'speaker tuple. Only 1 speaker label, '
                              f'\"{speaker}\", found in {self} '
                              f'yet there are {len(pairs_with_speaker)} '
                               'speaker tuples that have this speaker in '
                              f'them: {pairs_with_speaker}')
            elif not pairs_with_speaker:
                raise ValueError('No speaker tuple found containing speaker '
                                f'label \"{speaker}\".')
            return pairs_with_speaker[0]
        # If all elements in some speaker pair are in the speaker set, we 
        # assume we've found the right pair
        for pair in SPEAKER_PAIRS:
            if all(speaker in pair for speaker in self.speaker_set()):
                return pair
        # If we still haven't found a match, something has gone wrong
        raise ValueError(f'No valid speaker pair found for {self}. '
                         f'Speakers: {self.speaker_set}')

    @cached_property
    def _row_speakers(self) -> list[str | None]:
        """
        Returns a list where index in this list corresponds to a row in the 
        document, and each index in the list contains the speaker of that row.
        This list can be thought of as a mapping between each row index and the
        speaker of the row corresponding to each index.
        """
        row_speakers: list[str | None] = [None] * len(self.lines)
        current_speaker: str | None = None
        for i in range(len(self.lines)):
            line = self.lines[i]
            speaker_matches = self.find_speakers(line)
            # If speaker found, change global current_speaker variable
            if speaker_matches:
                # Check: a single line should only have one speaker.
                # If multiple speakers found, warn and use the first one
                if len(speaker_matches) > 1:
                    warnings.warn(
                        f'Multiple speakers found in row {i} of '
                        f'{self}. Speakers: {speaker_matches}. '
                         'Using first speaker.')
                # TODO: Warn if speaker is found not at the beginning of the 
                # line, ignoring timestamps
                current_speaker = speaker_matches[0]
            row_speakers[i] = current_speaker
            # If we've found a speaker farther than at the first row,
            # and the first row is empty, we assume that all rows up to this
            # point haven't been labeled (check)
            if i > 0 and current_speaker and not row_speakers[0]:
                assert row_speakers[:i] == [None] * i, \
                    f'Row speakers up to row {i} in {self} ' \
                    f'are not all None: {row_speakers}'
                # In the case when there are two speakers, we know the
                # empty rows are spoken by the other speaker.
                if len(self.speaker_tuple) == 2:
                    current_speaker_ind = (self.speaker_tuple
                                               .index(current_speaker))
                    other_speaker = self.speaker_tuple[current_speaker_ind-1]
                    row_speakers[:i] = [other_speaker] * i
                else:
                    warnings.warn(f'First few rows empty in {self} but there '
                                   'are too many speakers! I don\'t know how '
                                   'to fill them.')
        
        rows_without_speakers = tuple(i for i in range(len(row_speakers)) 
                                      if not row_speakers[i])
        if any(rows_without_speakers):
            warnings.warn(f'Rows {rows_without_speakers} in {self} '
                          f'are missing speakers.')
        return row_speakers
    
    @cached_property
    def _row_speakers_default(self) -> list[str]:
        """
        Convert all names in _row_speakers to their default pair names given
        by SPEAKER_PAIRS[0].
        """
        # See default_speaker_pair definition for convention
        default_interviewer_name = Document.default_speaker_pair[0]
        default_participant_name = Document.default_speaker_pair[1]
        last_speaker_in_pair = self.speaker_tuple[-1]
        return [default_participant_name if speaker == last_speaker_in_pair 
                else default_interviewer_name 
                for speaker in self._row_speakers]

    @cached_property
    def _labels(self) -> list[tuple[str, str]]:
        """
        Expects a list of label data from the datasaur document,
        Returns the tuple 
            (label_name, speaker),
        where label is the label's name and speaker is the label's speaker.
        """
        labels_with_speakers = [('', '')] * len(self.label_data)

        for k in range(len(self.label_data)):
            label = self.label_data[k]

            label_name = label['labelItem']['labelName']
            row_index = label['textPosition']['start']['row']
            speaker = self._row_speakers_default[row_index] 
            if not speaker:
                warnings.warn(
                    f'No speaker found for {label_name} label in row '
                    f'{row_index} of {self}.')
            labels_with_speakers[k] = (label_name, speaker)

        return labels_with_speakers

    @cached_property
    def label_counts(self) -> dict[str, str]:
        cntDict = Counter(self._labels)
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
            if not self.find_speakers(token)
        ]
        return ling.type_token_ratio(tokens)

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
                if self.find_speakers(token):
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
    
    def __repr__(self) -> str:
        return f'Document(name=\"{self.name}\", project=\"{self.project}\")'
