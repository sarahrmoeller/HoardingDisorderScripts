from utils.process_project import load_project_data
from utils.process_labeled_document import load_label_data

# Test with a sample project directory
project_dir = "data/HD_set1_1-7-NDE5MzE1ZWM"
project_data = load_project_data(project_dir)

# Print the results
print("Project ID:", project_data['id'])
print("Project Title:", project_data['title']) 
print("\nUsers:")
for user in project_data['users']:
    print(f"- {user['email']} ({user['role']})")

print("")
print("")

document_dir = project_dir + "/Document-" + project_data['users'][0]['parsed_email']
labeled_data = load_label_data(document_dir, project_data['users'][0]['documents'][0])

print("Path:", document_dir)
print("Document:", project_data['users'][0]['documents'][0])
print("User ID:", labeled_data['user']['id'])
print("User Email:", labeled_data['user']['email'])
print("First Token Set:", labeled_data['rows'][0][0])

print("")

print("First Span Label ID:", labeled_data['spans'][0]['labelId'])
print(
    "First Span Label Name:",
    [item for item in labeled_data['labels'] if item.get('id')==labeled_data['spans'][0]['labelId']][0]['labelName']
)
print("First Span Rejected:", labeled_data['spans'][0]['rejected'])
print(
    "First Span Start:",
    labeled_data['rows']
    [labeled_data['spans'][0]['start']['row']]
    [labeled_data['spans'][0]['start']['column']]
    [labeled_data['spans'][0]['start']['tokenIndex']]
)
print(
    "First Span End:",
    labeled_data['rows']
    [labeled_data['spans'][0]['end']['row']]
    [labeled_data['spans'][0]['end']['column']]
    [labeled_data['spans'][0]['end']['tokenIndex']]
)
