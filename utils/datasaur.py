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