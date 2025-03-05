import json
import os
import re

def load_project_data(directory):
    file_path = os.path.join(directory, 'project-data.json')
    with open(file_path, 'r') as file:
        raw_data = json.load(file)

    data = {}  # Use dictionary syntax instead of attribute access
    data['id'] = raw_data['project']['id']  # Access raw_data not data
    data['title'] = raw_data['project']['title']
    data['users'] = []

    for assignment in raw_data['project']['assignments']:
        user_info = {
            'id': assignment['id'],
            'email': assignment['email'], 
            'role': assignment['role'],
            'parsed_email': re.sub(r'[^a-zA-Z0-9]', '_', assignment['email'])
        }

        if ('documentInfos' in assignment):
            user_info['documents'] = []

            for document in assignment['documentInfos']:
                user_info['documents'].append(document['name'])

        data['users'].append(user_info)


    return data
