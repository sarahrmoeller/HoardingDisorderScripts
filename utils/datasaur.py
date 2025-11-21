from .document import Document
import os
from .project import projects, review_dir


by_project = {project: [Document(review_dir(project) + filename) 
                        for filename in os.listdir(review_dir(project))] 
              for project in projects}

by_doc = [doc for doc_list in by_project.values() for doc in doc_list]