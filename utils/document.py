from collections import Counter
from functools import cached_property
from itertools import product
import json
import os
import warnings
from . import regexes
from .regexes import SPEAKER_PAIRS, SPEAKERS
import string


# List of all labels (types of incomplete clauses) found across all projects
LABELS = {
    'Incomplete Thought',
    'Self Correction',
    'Clarification',
    'Generic Disfluency',
    'Misspeak',
    'Unclear',
    'Overlap'
}


class RawDocument:
    """
    Read-only class that provides information relevant to us given a raw-text
    document.
    """

    default_speaker_pair = regexes.SPEAKER_PAIRS[0]

    def __init__(self, path: str) -> None:
        with open(path) as f:
            self.full_lines = f.readlines()
        self.full_text = '\n'.join(self.full_lines)
        self.path = path
        self.name = os.path.basename(path)

    def clean_lines(self, lines, 
                    remove_timestamps=True,
                    do_replacements=True,
                    do_removals=True,
                    speaker_labels=False, remove_punctuation=False, 
                    lower=False) -> list[str]:
        """
        Big function to clean lines according to specified parameters.
        """
        if remove_timestamps == True:
            # Remove timestamps from the lines
            lines = [regexes.timestamps.sub('', line).strip()
                        for line in lines]
        if do_replacements == True:
            # Replace bracketed stuff with better representations
            lines = [regexes.replace_tokens(line)
                        for line in lines]
        if do_removals == True:
            # Remove tokens that are not useful for us
            lines = [regexes.remove_tokens(line)
                        for line in lines]
        if speaker_labels == True:
            # Remove speaker labels from the lines
            lines = [regexes.speaker_labels_restricted.sub('', line)
                     for line in lines]
        if lower == True:
            lines = [line.lower() for line in lines]
        if remove_punctuation == True:
            # Remove punctuation
            lines = [line.translate(str.maketrans('', '', string.punctuation))
                     for line in lines]
        # Remove empty lines
        lines = [line for line in lines if line]
        return lines

    def lines(self, 
              speaker: None | str=None, cleaned=True, 
              remove_timestamps=True, do_replacements=True, do_removals=True,
              speaker_labels=False, remove_punctuation=False, lower=False
        ) -> list[str]:
        """
        Returns a dictionary where keys are speaker names and values are lists
        of lines spoken by that speaker.
        """
        # If no speaker is specified...
        if speaker is None:
            # And the user asks to clean, return all lines with cleaning 
            # applied
            if cleaned:
                return self.clean_lines(self.full_lines, 
                                        remove_timestamps=remove_timestamps, 
                                        do_replacements=do_replacements, 
                                        do_removals=do_removals, 
                                        speaker_labels=speaker_labels, 
                                        remove_punctuation=remove_punctuation, 
                                        lower=lower)
            # If the user doesn't ask to clean, return all lines as-is
            return self.full_lines
        # Otherwise, if a speaker label is specified, make sure the label 
        # is known 
        assert speaker in SPEAKERS, f"Speaker label {speaker} not known." \
                                    f"({self})"
        # also make sure the label is in the standard format (that I set in 
        # self.default_speaker_pair)
        assert speaker in self.default_speaker_pair, \
            f"Speaker label {speaker} not in default speaker pair " \
            f"{self.default_speaker_pair}, check spelling? ({self})"
        # Filter full lines to only those spoken by the specified speaker
        speaker_lines = [self.full_lines[i] 
                         for i in range(len(self.full_lines))
                         if self._row_speakers_default[i] == speaker]
        # If the user asks to clean, clean the speaker lines before 
        # returning them
        if cleaned:
            speaker_lines = self.clean_lines(speaker_lines, 
                                        remove_timestamps=remove_timestamps, 
                                        do_replacements=do_replacements, 
                                        do_removals=do_removals, 
                                        speaker_labels=speaker_labels, 
                                        remove_punctuation=remove_punctuation, 
                                        lower=lower)
        return speaker_lines

    def content(self, 
                speaker: None | str=None, cleaned=True, 
                remove_timestamps=True, do_replacements=True, do_removals=True,
                speaker_labels=False, remove_punctuation=False, lower=False
        ) -> str:
        """
        Returns a dictionary where keys are speaker names and values are lists
        of lines spoken by that speaker.
        """
        content = '\n'.join(self.lines(speaker, cleaned=cleaned,
                         remove_timestamps=remove_timestamps, 
                         do_replacements=do_replacements, 
                         do_removals=do_removals, 
                         speaker_labels=speaker_labels, 
                         remove_punctuation=remove_punctuation, 
                         lower=lower))
        return content

    def speaker_set(self, restrict=True) -> set[str]:
        """
        Returns the set of all speaker labels found in the document.
        If the restrict flag is set to False, all strings appearing to be
        speaker labels (those strings captured by `regexes.find_speakers`) will
        be returned.
        """
        speaker_matches = regexes.find_speakers(self.full_text, 
                                                restrict=restrict)
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
        lines = self.lines(cleaned=False)
        row_speakers: list[str | None] = [None] * len(lines)
        current_speaker: str | None = None
        for i in range(len(lines)):
            line = lines[i]
            speaker_matches = regexes.find_speakers(line)
            # If speaker found, change global current_speaker variable
            if speaker_matches:
                # In the case that len(speaker_matches) > 1, we use the last 
                # entry in the list so that the next line is most up-to-date
                current_speaker = speaker_matches[-1]
            row_speakers[i] = current_speaker
            # If we've found a speaker farther than at the first row,
            # and the first row is empty, we assume that all rows up to this
            # point haven't been labeled (check)
            if i > 0 and current_speaker and not row_speakers[0]:
                # In the case when there are two speakers, we know the
                # empty rows are spoken by the other speaker.
                if len(self.speaker_tuple) == 2:
                    current_speaker_ind = (self.speaker_tuple
                                               .index(current_speaker))
                    other_speaker = self.speaker_tuple[current_speaker_ind-1]
                    row_speakers[:i] = [other_speaker] * i
                else:
                    warnings.warn(f'First {i+1} rows (out of '
                                  f'{len(lines)}) empty in {self}, but '
                                   'there are too many speakers! I don\'t '
                                   'know how to fill them.')
        
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

class Document:
    """
    Read-only class that provides information relevant to us given a datasaur
    document.
    """

    # Define the default speaker names to use for display in output table
    # Default interviewer name is at index 0, and default participant name is
    # at index 1
    default_speaker_pair = regexes.SPEAKER_PAIRS[0]
        
    def __init__(self, path: str) -> None:
        with open(path) as f:
            self.json_dump = json.load(f)
        self.path = path
        # JSON always looks like {'version' : '1.0', 'data' : {...}},
        # So we will just index into the 'data' key
        self.data = self.json_dump['data']
        self.project = self.data['project']['name']
        self.name = self.data['document']['name']
        self.transcript_number = self.name.split('_')[0]
        self.set = 1 if self.name[0] == '0' else int(self.name[0])
        assert self.set in (1, 2, 3)
        self.fixed_name = self.name
        if self.set == 1:
            self.fixed_name = f'1{self.name}'
        self.hoarder_flag = int(self.set == 1)
        # To make it easy to read document properties while debugging
        # Accessing the first element of the row since all rows are singleton
        # lists
        self.row_data: list[dict] = [row[0] for row in self.data['rows']]
        # List of rows in the document indexed by carriage returns
        self.tokens = [row['tokens'] for row in self.row_data]
        self.label_data = self.data['spanLabels']

    def write_to_file(self, dir: str='.', 
                      speaker: None | str=None, cleaned=True, 
                      remove_timestamps=True, do_replacements=True, 
                      do_removals=True, speaker_labels=False, 
                      remove_punctuation=False, lower=False) -> None:
        """
        Write the document to a file. 
        Writes to the (optionally) specfied directory. If no directory is 
        specified, writes to the current directory.
        """
        content = self.content(speaker, cleaned=cleaned,
                         remove_timestamps=remove_timestamps, 
                         do_replacements=do_replacements, 
                         do_removals=do_removals, 
                         speaker_labels=speaker_labels, 
                         remove_punctuation=remove_punctuation, 
                         lower=lower)
        with open(f"{dir}/{self.name}", 'w') as f:
            f.write(content)
    
    def clean_lines(self, lines, 
                    remove_timestamps=True,
                    do_replacements=True,
                    do_removals=True,
                    speaker_labels=False, remove_punctuation=False, 
                    lower=False) -> list[str]:
        """
        Big function to clean lines according to specified parameters.
        """
        if remove_timestamps == True:
            # Remove timestamps from the lines
            lines = [regexes.timestamps.sub('', line).strip()
                        for line in lines]
        if do_replacements == True:
            # Replace bracketed stuff with better representations
            lines = [regexes.replace_tokens(line)
                        for line in lines]
        if do_removals == True:
            # Remove tokens that are not useful for us
            lines = [regexes.remove_tokens(line)
                        for line in lines]
        if speaker_labels == True:
            # Remove speaker labels from the lines
            lines = [regexes.speaker_labels_restricted.sub('', line)
                     for line in lines]
        if lower == True:
            lines = [line.lower() for line in lines]
        if remove_punctuation == True:
            # Remove punctuation
            lines = [line.translate(str.maketrans('', '', string.punctuation))
                     for line in lines]
        # Remove empty lines
        lines = [line for line in lines if line]
        return lines

    def lines(self, 
              speaker: None | str=None, cleaned=True, 
              remove_timestamps=True, do_replacements=True, do_removals=True,
              speaker_labels=False, remove_punctuation=False, lower=False
        ) -> list[str]:
        """
        Returns a dictionary where keys are speaker names and values are lists
        of lines spoken by that speaker.
        """
        lines = [ row['content'].rstrip() for row in self.row_data ]
        if speaker is None:
            if cleaned:
                lines = self.clean_lines(lines, 
                                         remove_timestamps=remove_timestamps, 
                                         do_replacements=do_replacements, 
                                         do_removals=do_removals, 
                                         speaker_labels=speaker_labels, 
                                         remove_punctuation=remove_punctuation, 
                                         lower=lower)
            return lines
        assert speaker in SPEAKERS, f"Speaker label {speaker} not known." \
                                    f"({self})"
        assert speaker in self.default_speaker_pair, \
            f"Speaker label {speaker} not in default speaker pair " \
            f"{self.default_speaker_pair}, check spelling? ({self})"
        speaker_lines = [lines[i] for i in range(len(lines))
                         if self._row_speakers_default[i] == speaker]
        if cleaned:
            speaker_lines = self.clean_lines(speaker_lines, 
                                        remove_timestamps=remove_timestamps, 
                                        do_replacements=do_replacements, 
                                        do_removals=do_removals, 
                                        speaker_labels=speaker_labels, 
                                        remove_punctuation=remove_punctuation, 
                                        lower=lower)
        return speaker_lines

    def content(self, 
                speaker: None | str=None, cleaned=True, 
                remove_timestamps=True, do_replacements=True, do_removals=True,
                speaker_labels=False, remove_punctuation=False, lower=False
        ) -> str:
        """
        Returns a dictionary where keys are speaker names and values are lists
        of lines spoken by that speaker.
        """
        content = '\n'.join(self.lines(speaker, cleaned=cleaned,
                         remove_timestamps=remove_timestamps, 
                         do_replacements=do_replacements, 
                         do_removals=do_removals, 
                         speaker_labels=speaker_labels, 
                         remove_punctuation=remove_punctuation, 
                         lower=lower))
        return content

    def speaker_set(self, restrict=True) -> set[str]:
        """
        Returns the set of all speaker labels found in the document.
        If the restrict flag is set to False, all strings appearing to be
        speaker labels (those strings captured by `regexes.find_speakers`) will
        be returned.
        """
        speaker_matches = regexes.find_speakers(self.content(cleaned=False), 
                                                restrict=restrict)
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
        lines = self.lines(cleaned=False)
        row_speakers: list[str | None] = [None] * len(lines)
        current_speaker: str | None = None
        for i in range(len(lines)):
            line = lines[i]
            speaker_matches = regexes.find_speakers(line)
            # If speaker found, change global current_speaker variable
            if speaker_matches:
                # In the case that len(speaker_matches) > 1, we use the last 
                # entry in the list so that the next line is most up-to-date
                current_speaker = speaker_matches[-1]
            row_speakers[i] = current_speaker
            # If we've found a speaker farther than at the first row,
            # and the first row is empty, we assume that all rows up to this
            # point haven't been labeled (check)
            if i > 0 and current_speaker and not row_speakers[0]:
                # In the case when there are two speakers, we know the
                # empty rows are spoken by the other speaker.
                if len(self.speaker_tuple) == 2:
                    current_speaker_ind = (self.speaker_tuple
                                               .index(current_speaker))
                    other_speaker = self.speaker_tuple[current_speaker_ind-1]
                    row_speakers[:i] = [other_speaker] * i
                else:
                    warnings.warn(f'First {i+1} rows (out of '
                                  f'{len(lines)}) empty in {self}, but '
                                   'there are too many speakers! I don\'t '
                                   'know how to fill them.')
        
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
    
    def __repr__(self) -> str:
        return f"Document({self.name}, {self.project})"