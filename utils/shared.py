from typing import Callable
import warnings


def get_row_speakers(
    lines: list[str],
    speaker_tuple: tuple[str, ...],
    find_speakers: Callable,
    name: str,
    project: str = ''
) -> list[str | None]:
    """
    Returns a list where index in this list corresponds to a row in the 
    document, and each index in the list contains the speaker of that row.
    This list can be thought of as a mapping between each row index and the
    speaker of the row corresponding to each index.
    """
    project = f'({project})' if project else '' # For error messaging

    row_speakers: list[str | None] = [None] * len(lines)
    current_speaker: str | None = None
    for i in range(len(lines)):
        line = lines[i]
        speaker_matches = find_speakers(line)
        # If speaker found, change global current_speaker variable
        if speaker_matches:
            # Check: a single line should only have one speaker.
            # If multiple speakers found, warn and use the first one
            if len(speaker_matches) > 1:
                warnings.warn(
                    f'Multiple speakers found in row {i} of document '
                    f'{name} (Project {project}). Speakers: '
                    f'{speaker_matches}. Using first speaker.'
                )
            # TODO: Warn if speaker is found not at the beginning of the 
            # line, ignoring timestamps
            current_speaker = speaker_matches[0]
        row_speakers[i] = current_speaker
        # If we've found a speaker farther than at the first row,
        # and the first row is empty, we assume that all rows up to this
        # point haven't been labeled (check)
        if i > 0 and current_speaker and not row_speakers[0]:
            assert row_speakers[:i] == [None] * i, \
                f'Row speakers up to row {i} in {name} ' \
                f'({project}) are not all None: {row_speakers}'
            # In the case when there are two speakers, we know the
            # empty rows are spoken by the other speaker.
            if len(speaker_tuple) == 2:
                current_speaker_ind = (speaker_tuple
                                            .index(current_speaker))
                other_speaker = speaker_tuple[current_speaker_ind-1]
                row_speakers[:i] = [other_speaker] * i
            else:
                warnings.warn(f'First few rows empty in {name} '
                                f'{project}, but there are too many '
                                'speakers! I don\'t know how to fill them.')
    
    rows_without_speakers = tuple(i for i in range(len(row_speakers)) 
                                    if not row_speakers[i])
    if any(rows_without_speakers):
        warnings.warn(f'Rows {rows_without_speakers} in {name} '
                        f'{project} are missing speakers.')
    return row_speakers