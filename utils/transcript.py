from .document import Document
from . import datasaur as data


class Transcript(Document):
    """
    A class to represent a transcript, which is a collection of documents
    with the same transcript number.
    """

    def __init__(self, transcript_number: str) -> None:
        assert transcript_number in data.transcript_numbers, \
            f'Transcript number {transcript_number} not found in available ' \
             'transcripts.'
        self.transcript_number = transcript_number
        # All documents associated with this transcript number
        # i.e. if transcript_number is "005", then this will have
        # '005_082', '005_083', '005_086', etc.
        self.docs: list[Document] = [
            doc for doc in data.by_doc 
            if doc.transcript_number == self.transcript_number
        ]
        assert self.docs, \
            f"No documents found for transcript number {transcript_number}"
        self.docs.sort(key=lambda doc: doc.name) # Sorted for easier debugging
        self.set = self.docs[0].set
        self.hoarder_flag = self.docs[0].hoarder_flag
        self.row_data = [rd for doc in self.docs for rd in doc.row_data]
        self.lines = [line for doc in self.docs for line in doc.lines]
        self.content = "\n".join(doc.content for doc in self.docs)
    
    def write_to_file(self, path: str='') -> None:
        """
        Write the transcript to a file. 
        """
        path = path or f"./{self.transcript_number}.txt"
        with open(path, 'w') as f:
            f.write(self.content)

    def __repr__(self) -> str:
        return f"Transcript(\"{self.transcript_number}\")"