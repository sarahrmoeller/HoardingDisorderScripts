import utils.raw as raw
import re
from utils.document import RawDocument


if __name__ == "__main__":
    for doc_path in raw.doc_paths:
        doc = RawDocument(doc_path)
        if re.search(r'Interviewer\d', doc.content()):
            print(f"Document {doc.name} has Interviewer\\d in content.") 
            with open(doc_path, 'w') as f:
                f.write(re.sub(r'Interviewer\d', 'Interviewer', doc.content()))
