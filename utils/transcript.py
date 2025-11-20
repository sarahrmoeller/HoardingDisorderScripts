from .document import Document
from . import datasaur as data
from functools import cached_property
from collections import Counter


transcript_numbers = sorted(list(set(doc.transcript_number 
                                     for doc in data.by_doc)))


class Transcript(Document):
    """
    A class to represent a transcript, which is a collection of documents
    with the same transcript number.
    """

    def __init__(self, transcript_number: str) -> None:
        assert transcript_number in transcript_numbers, \
            f'Transcript number {transcript_number} not found in available ' \
             'transcripts.'
        self.number = transcript_number
        # All documents associated with this transcript number
        # i.e. if transcript_number is "005", then this will have
        # '005_082', '005_083', '005_086', etc.
        self.docs: list[Document] = [
            doc for doc in data.by_doc 
            if doc.transcript_number == self.number
        ]
        assert self.docs, \
            f"No documents found for transcript number {transcript_number}"
        # Sorted so transcript order is preserved
        self.docs.sort(key=lambda doc: doc.name) 
        self.set = self.docs[0].set
        self.hoarder_flag = self.docs[0].hoarder_flag
        # Extracting data from all documents, flattening the lists
        self.row_data = [rd for doc in self.docs for rd in doc.row_data]
        self.label_data = [ld for doc in self.docs for ld in doc.label_data]
    
    def lines(self, 
              speaker: None | str=None, cleaned=True, 
              remove_timestamps=True, do_replacements=True, do_removals=True,
              speaker_labels=False, remove_punctuation=False, lower=False
              ) -> list[str]:
        """
        Get all lines from all documents in the transcript.
        """
        return [line for doc in self.docs
                for line in doc.lines(speaker=speaker, cleaned=cleaned, 
                   remove_timestamps=remove_timestamps, 
                   do_replacements=do_replacements, 
                   do_removals=do_removals,
                   speaker_labels=speaker_labels, 
                   remove_punctuation=remove_punctuation, 
                   lower=lower)]
    
    def content(self,
                speaker: None | str=None, cleaned=True, 
                remove_timestamps=True, do_replacements=True, do_removals=True,
                speaker_labels=False, remove_punctuation=False, lower=False
                ) -> str:
        """
        Get the full content of the transcript by concatenating the content
        of all documents in the transcript.
        """
        return '\n'.join(doc.content(speaker=speaker, cleaned=cleaned, 
                                     remove_timestamps=remove_timestamps, 
                                     do_replacements=do_replacements, 
                                     do_removals=do_removals,
                                     speaker_labels=speaker_labels, 
                                     remove_punctuation=remove_punctuation, 
                                     lower=lower)
                         for doc in self.docs)
    
    def write_to_file(self, dir: str='.', speaker: None | str=None, 
                      cleaned=True, 
                      remove_timestamps=True, do_replacements=True, 
                      do_removals=True, speaker_labels=False, 
                      remove_punctuation=False, lower=False
                    ) -> None:
        """
        Write the transcript to a file. 
        Writes to the (optionally) specfied directory. If no directory is 
        specified, writes to the current directory.
        """
        with open(f"{dir}/{self.number}.txt", 'w') as f:
            f.write(self.content(speaker=speaker, cleaned=cleaned, 
                                 remove_timestamps=remove_timestamps, 
                                 do_replacements=do_replacements, 
                                 do_removals=do_removals,
                                 speaker_labels=speaker_labels, 
                                 remove_punctuation=remove_punctuation, 
                                 lower=lower))
    
    @cached_property
    def label_counts_tr(self) -> dict[str, int]:
        summed_counter = Counter()
        for doc in self.docs:
            summed_counter.update(doc.label_counts)
        return dict(summed_counter)

    def __getitem__(self, index: str) -> Document:
        """
        Get a document by its index within the transcript.
        
        Ex: if you want document '2008_118', access Transcript('2008')['118'].
        """
        for doc in self.docs:
            if doc.name == f"{self.number}_{index}.txt":
                return doc
        raise KeyError(f"Document no. {index} "
                       f"('{self.number}_{index}.txt') not found "
                       f"in transcript {self.number}")

    def __repr__(self) -> str:
        return f"Transcript(\"{self.number}\")"