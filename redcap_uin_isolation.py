import json
import requests
from datetime import datetime
import os

def redcap_uin_isloation(records):
    # Fetch REDCap record for given uin and load it into dictionary
    for record in records:
        data = {
            'token': os.environ.get("REDCAP_TOKEN"),
            'content': 'record',
            'format': 'json',
            'type': 'flat',
            'csvDelimiter': '',
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'exportSurveyFields': 'false',
            'exportDataAccessGroups': 'false',
            'returnFormat': 'json',
            'filterLogic': '[uin] = ' + record["uin"]
        }
        r = requests.post(os.environ.get("REDCAP_ENDPOINT"),data=data)
        print('HTTP Status: ' + str(r.status_code) + " Connected to QIR for download")
        if len(r.json()) == 0:
            continue
        rdict = dict(r.json()[0])
        if record["Result"] == "1":
            rdict['pos_date'] = datetime.strptime(record["ResultDate"], '%Y-%m-%dT%H:%M:%S.%f%z').strftime('%m/%d/%Y')
            rdict['test_status'] = "2"

            # Serializae the json
            import_json = json.dumps([rdict])
            # Set parameters for the upload
            data = {
                'token': os.environ.get("REDCAP_TOKEN"),
                'content': 'record',
                'format': 'json',
                'type': 'flat',
                'overwriteBehavior': 'normal',
                'forceAutoNumber': 'false',
                'data': import_json,
                'dateFormat': 'MDY',
                'returnContent': 'count',
                'returnFormat': 'json'
            }

            # Post the upload and print the connection status
            r = requests.post(os.environ.get("REDCAP_ENDPOINT"),data=data)
            print('HTTP Status: ' + str(r.status_code) + " Connected to QIR for upload")

