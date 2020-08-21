# still in progress

#!/usr/bin/env python
import requests
import json
import os


def REDCapMedicatImport(meddata):
    # REDCap parameters
    exportdata = {
        'token': os.environ.get("REDCAP_MEDICAT_TOKEN"),
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'fields[0]': 'record_id',
        'fields[1]': 'uin',
        'forms[0]': 'test_results',
        'events[0]': 'presurvey_arm_1',
        'events[1]': 'samples_arm_1',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }

    # exported data from source project
    exportr = requests.post('https://redcap-test.healthinstitute.illinois.edu/api/', data=exportdata)

    # create data strcutures to accumulate values
    records_dict_list = []

    # check connection
    if str(exportr.status_code) == '200':
        # define the dict to hold the records
        records_dict = {}
        for record in exportr.json():
            # define list to hold record values
            repeat_instances = []
            # add records to dict that don't already exsit
            if record['record_id'] not in records_dict.keys():
                # add the record id as the dict key
                records_dict[record['record_id']] = []
                if record['uin'] != "":
                    for u in meddata:
                        # match the UINs
                        if record['uin'] == u['UIN']:
                            # append UIN and repeat instance number
                            repeat_instances.append(record['uin'])
                            if record['redcap_repeat_instance'] != "":
                                repeat_instances.append(record['redcap_repeat_instance'])
                                # add the record to the dict
                            records_dict[record['record_id']] = records_dict[record['record_id']] = [repeat_instances[0], repeat_instances[1:]]
            else:
                # if the record is in the dict, add the latest instance
                records_dict[record['record_id']].append(record['redcap_repeat_instance'])
    else:
        print('HTTP Status: ' + str(exportr.status_code))

    for i in range(len(records_dict)):
        # iterate through each record to build new json
        for u in meddata:
            med_dict = {}
            if u['UIN'] in list(records_dict.values())[i]:
                med_dict['record_id'] = list(records_dict.keys())[i]
                med_dict['redcap_event_name'] = 'samples_arm_1'
                med_dict['redcap_repeat_instrument'] = 'test_results'
                # increment each instance by one
                if isinstance(list(records_dict.values())[i][-1], int):
                    med_dict['redcap_repeat_instance'] = list(records_dict.values())[i][-1] + 1
                else:
                    # assign one to records with no repeat instances
                    med_dict['redcap_repeat_instance'] = 1
                med_dict['result'] = u['Result']
                med_dict['order_date'] = u['OrderDate']
                med_dict['result_date'] = u['ResultDate']
                med_dict['test_results_complete'] = 2
                # append the dict to a list
                records_dict_list.append(med_dict)

    # convert dict to json format
    app_json = json.dumps(records_dict_list)

    # Import data into REDCap
    importdata = {
        'token': os.environ.get("REDCAP_MEDICAT_TOKEN"),
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'overwriteBehavior': 'normal',
        'forceAutoNumber': 'false',
        'data': app_json,
        'returnContent': 'count',
        'returnFormat': 'json'
        }

    importr = requests.post(os.environ.get("https://redcap-test.healthinstitute.illinois.edu/api/"),data= importdata)
