from utils.process_project import load_project_data
from utils.process_labeled_document import load_label_data

project_dir = "data/HD_set1_1-7-NDE5MzE1ZWM" # TODO: Remove Hardcoded Value
project_data = load_project_data(project_dir)

document_label_cnts = {}

for user in project_data['users']:
    user_document_dir = project_dir + "/DOCUMENT-" + user['parsed_email']
    if 'documents' not in user.keys():
        continue

    for document in user['documents']:
        labeled_data = load_label_data(user_document_dir, document)

        if document not in document_label_cnts:
            document_label_cnts[document] = {}
        
        for span in labeled_data['spans']:
            label_id = [
                label for label in labeled_data['labels'] if label['id'] == span['labelId']
            ][0]['labelName']
            if label_id not in document_label_cnts[document]:
                document_label_cnts[document][label_id] = {}
                document_label_cnts[document][label_id]['accepted'] = 0
                document_label_cnts[document][label_id]['rejected'] = 0
            
            if span['accepted']:
                document_label_cnts[document][label_id]['accepted'] += 1
            else:
                document_label_cnts[document][label_id]['rejected'] += 1

print("")
print("")

# Print the results sorted alphabetically
for document in sorted(document_label_cnts.keys()):
    print(f"Document: {document}")
    total_accepted = 0
    total_rejected = 0
    for label in sorted(document_label_cnts[document].keys()):
        print(f"- {label}: {document_label_cnts[document][label]['accepted']} + {document_label_cnts[document][label]['rejected']}")
        total_accepted += document_label_cnts[document][label]['accepted']
        total_rejected += document_label_cnts[document][label]['rejected']
    print(f"Total: {total_accepted} + {total_rejected}")
    print("")
