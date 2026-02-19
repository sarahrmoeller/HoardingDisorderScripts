import os


project_dir_locations = ('./data/mathews/documents/datasaur_exports/' + 
                         'truncated_clauses')
projects = [d for d in os.listdir(project_dir_locations)
            if os.path.isdir(os.path.join(project_dir_locations, d))]

def review_dir(project: str) -> str:
    """
    Given name of a project, return the path to the REVIEW directory
    assuming current directory is the project's root.

    Example: "HD_set1_1-7" -> "./{project_dir_locations}/HD_set1_1-7/REVIEW/"
    """
    return f"{project_dir_locations}/{project}/REVIEW/"
