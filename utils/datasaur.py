from .document import Document
import os


project_dir_locations = ('./data/mathews/documents/datasaur_exports/' + 
                         'truncated_clauses')
projects = os.listdir(project_dir_locations)

def review_dir(project: str) -> str:
    """
    Given name of a project, return the path to the REVIEW directory
    assuming current directory is the project's root.

    Example: "HD_set1_1-7" -> "./{project_dir_locations}/HD_set1_1-7/REVIEW/"
    """
    return f"{project_dir_locations}/{project}/REVIEW/"

by_project = {project: [Document(review_dir(project) + filename) 
                        for filename in os.listdir(review_dir(project))] 
              for project in projects}

by_doc = [doc for doc_list in by_project.values() for doc in doc_list]

transcript_numbers = sorted(list(set(doc.transcript_number for doc in by_doc)))
by_transcript = {tn : sorted([doc for doc in by_doc
                              if doc.transcript_number == tn],
                             key=lambda doc: doc.name)
                 for tn in transcript_numbers}
