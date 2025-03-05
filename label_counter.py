from utils.process_project import load_project_data
from utils.process_labeled_document import load_label_data

project_dir = "data/HD_set1_1-7-NDE5MzE1ZWM" # TODO: Remove Hardcoded Value
project_data = load_project_data(project_dir)

documents = {}

for user in project_data['users']:
    document_dir = project_dir + "/Document-" + user['parsed_email']
    if 'documents' not in user:
        continue

    for document in user['documents']:
        labeled_data = load_label_data(document_dir, document)

        if document not in documents:
            documents[document] = {}
        
        for span in labeled_data['spans']:
            label_id = [item for item in labeled_data['labels'] if item.get('id')==span['labelId']][0]['labelName']
            if label_id not in documents[document]:
                documents[document][label_id] = {}
                documents[document][label_id]['rejected'] = 0
                documents[document][label_id]['accepted'] = 0
            
            if span['rejected']:
                documents[document][label_id]['rejected'] += 1
            else:
                documents[document][label_id]['accepted'] += 1

print("")
print("")

# Print the results sorted alphabetically
for document in sorted(documents.keys()):
    print(f"Document: {document}")
    total_accepted = 0
    total_rejected = 0
    for label in sorted(documents[document].keys()):
        print(f"- {label}: {documents[document][label]['accepted']} + {documents[document][label]['rejected']}")
        total_accepted += documents[document][label]['accepted']
        total_rejected += documents[document][label]['rejected']
    print(f"Total: {total_accepted} + {total_rejected}")
    print("")
