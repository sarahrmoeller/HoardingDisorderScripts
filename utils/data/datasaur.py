from ..document import DatasaurDocument
import os
from .project import projects, review_dir


by_project = {project: [DatasaurDocument(review_dir(project) + filename) 
                        for filename in os.listdir(review_dir(project))] 
              for project in projects}

docs = [doc for doc_list in by_project.values() for doc in doc_list]
