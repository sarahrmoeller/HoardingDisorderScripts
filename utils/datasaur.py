from .document import Document
import os


projects = os.listdir('./data')
projects.remove('.gitignore')
# All files we care about are in the review dir
review_dir = lambda proj: f"./data/{proj}/REVIEW/"

data: dict[str, list] = {
    project: [Document(review_dir(project) + filename) 
              for filename in os.listdir(review_dir(project))]
    for project in projects
}
all_docs = [doc for doc_list in data.values() for doc in doc_list]

transcript_numbers = (doc.transcript_number for doc in all_docs)
docs_by_number = {tn : sorted([doc for doc in all_docs 
                               if doc.transcript_number == tn],
                               key=lambda d: d.name)
                  for tn in transcript_numbers}
