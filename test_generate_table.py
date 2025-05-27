from generate_table import Document


# Using this project directory for testing since it has files from sets 1-3
project_dir = "s1062_s2022-26_s3076-97"
# All files we care about are in the REVIEW directory
review_dir = f"./data/{project_dir}/REVIEW/" 
# One test file from each set
test_files = ["062_745.txt", "2022_335.txt", "3001_090.txt"]
test_docs = [Document(review_dir + filename + '.json') 
             for filename in test_files]


def test_row_speakers():
    ...