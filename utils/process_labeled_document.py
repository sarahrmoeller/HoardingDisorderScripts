import json
import os

def load_label_data(directory, file):
    file_path = os.path.join(directory, file + '.json')
    with open(file_path, 'r') as file:
        raw_data = json.load(file)
    
    data = {}

    # Base Data
    data['project'] = {}
    data['project']['id'] = raw_data['data']['project']['id']
    data['project']['name'] = raw_data['data']['project']['name']
    data['document'] = {}
    data['document']['id'] = raw_data['data']['document']['id']
    data['document']['name'] = raw_data['data']['document']['name']
    data['user'] = {}
    data['user']['name'] = raw_data['data']['labelerInfo']['displayName']
    data['user']['email'] = raw_data['data']['labelerInfo']['email']
    data['user']['id'] = raw_data['data']['labelerInfo']['id']

    # Labels
    data['labels'] = []
    for label in raw_data['data']['labelSets'][0]['labelItems']:
        label_info = {
            'id': label['id'],
            'labelName': label['labelName'],
        }
        data['labels'].append(label_info)
    
    # Rows
    data['rows'] = []
    speaker = ""
    for row in raw_data['data']['rows']:
        row_tokens = []

        for column in row:
            if (column['content'].find(":") != -1):
                speaker = column['content'].split(":")[0]
            
            row_tokens.append({
                'tokens': column['tokens'],
                'speaker': speaker,
            })
        
        data['rows'].append(row_tokens)

    # Spans
    data['spans'] = []
    for span in raw_data['data']['spanLabels']:
        span_info = {
            'id': span['id'],
            'labeledBy': span['labeledByUserId'],
            'acceptedBy': span['acceptedByUserId'],
            'rejectedBy': span['rejectedByUserId'],
            'accepted': span['status'] == 'ACCEPTED',
            'labelId': span['labelItem']['id'],
            'start': span['textPosition']['start'],
            'end': span['textPosition']['end'],
        }
        data['spans'].append(span_info)

    return data
