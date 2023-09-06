import hubspot
from dateutil import parser
from pprint import pprint
from hubspot.crm.contacts import PublicObjectSearchRequest, ApiException
from datetime import datetime, timedelta
import requests
import json
import logging


def read_entries(api_accesstoken, last_written_entry_timestamp):
    api_client = hubspot.Client.create(access_token=api_accesstoken)
    logging.info('read entries cutoff %s', last_written_entry_timestamp)
    date = str(int(parser.isoparse(last_written_entry_timestamp).timestamp() * 1000))
    public_object_search_request = PublicObjectSearchRequest(
        filter_groups=[
            {
                "filters": [
                    {
                        "value": date,
                        "propertyName": "lastmodifieddate",
                        "operator": "GT"
                    }
                ]
            }
        ], 
        limit=30,
        properties=[# 'adressgruppe', 'adressnummer', 'anrede'
                    'associatedCompanyId',                  
                    'k_alphaplan_adressnummer_hubspot', 
                    'k_alphaplan_ansprechpartnerid_hubspot',
                    'suchname', #2
                    'firstname', #3
                    'lastname', #4
                    'email', #5
                    'phone', #6
                    'salutation',#7
                    'fax', #8
                    'mobilephone', #9
                    'telefon_privat', #10
                    'website', #11
                    'abteilung', #12
                    'information', #13
                    'titel', #14
                    'address', #15
                    'zip', #16
                    'city', #17
                    'jobtitle' #18
                    ]
    )
    try:
        api_response = api_client.crm.contacts.search_api.do_search(
            public_object_search_request=public_object_search_request)
        new_entries = api_response.results
        json_entries = [entry.to_dict() for entry in new_entries]
        for entry in json_entries:
            entry['sortTimestamp'] = entry['properties']['lastmodifieddate']
        return json_entries
    except ApiException as e:
        print("Exception when calling search_api->do_search: %s\n" % e)

# def read_archived_entries(api_accesstoken, last_written_entry_timestamp):
#     url = "https://api.hubapi.com/crm/v3/objects/contacts?archived=true&limit=100&properties=hs_object_id,associatedCompanyId,k_alphaplan_adressnummer_hubspot,k_alphaplan_ansprechpartnerid_hubspot,suchname,firstname,lastname,email,phone,salutation,fax,mobilephone,telefon_privat,website,abteilung,information,titel,address,zip,city,jobtitle"
#     # Bearer token
#     bearer_token = api_accesstoken
#     # Set the request headers with the Bearer token
#     headers = {
#         "Authorization": f"Bearer {bearer_token}"
#     }
#     # Send the GET request with the headers
#     response = requests.get(url, headers=headers)
#     # Process the response
#     if response.status_code == 200:
#         data = response.json()        
#         entries = data['results']
#         logging.info('read archived entries cutoff %s', last_written_entry_timestamp)
#         filtered_list = [item for item in entries if item['archivedAt'] > last_written_entry_timestamp]
#         for entry in filtered_list:
#             entry['sortTimestamp'] = entry['archivedAt']
#         return filtered_list
#     else:
#         print(f"Request failed with status code: {response.status_code}")


def read_page_archived_entries(link, bearer_token):
    # Set the request headers with the Bearer token
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    # Send the GET request with the headers
    response = requests.get(link, headers=headers)
    # Process the response
    if response.status_code == 200:
        data = response.json()        
        entries = data['results']
        if 'paging' in data.keys():            
            next_link = data['paging']['next']['link']
        else:
            next_link = None
        return next_link, entries
    else:
        print(f"Request failed with status code: {response.status_code}")


def get_all_archived_entries(bearer_token):
    next_link = "https://api.hubapi.com/crm/v3/objects/contacts?archived=true&limit=100&properties=hs_object_id,associatedCompanyId,k_alphaplan_adressnummer_hubspot,k_alphaplan_ansprechpartnerid_hubspot,suchname,firstname,lastname,email,phone,salutation,fax,mobilephone,telefon_privat,website,abteilung,information,titel,address,zip,city,jobtitle"
    
    big_list = []
    b = 1
    while True:
        next_link, entries = read_page_archived_entries(next_link, bearer_token)
        logging.info(f'----- batch {b} of archived entries read')
        big_list.append(entries)
        b+=1
        if next_link == None:
            break
    flat_list = [item for sublist in big_list for item in sublist]
    return flat_list


def read_archived_entries(api_accesstoken, last_written_entry_timestamp):
    # Bearer token
    bearer_token = api_accesstoken
    # Set the request headers with the Bearer token
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    # get all archived entries
    all_archived_entries = get_all_archived_entries(bearer_token)
    # filter archived entries on 
    logging.info('read archived entries cutoff %s', last_written_entry_timestamp)
    filtered_list = [item for item in all_archived_entries if item['archivedAt'] > last_written_entry_timestamp]
    for entry in filtered_list:
            entry['sortTimestamp'] = entry['archivedAt']
    return filtered_list


def concat_and_sort(updated_entries, archived_entries):
    joined_entries = updated_entries + archived_entries
    joined_sorted_entries = sorted(joined_entries, key=lambda x: datetime.  \
                        strptime(x['sortTimestamp'], \
                                 '%Y-%m-%dT%H:%M:%S.%fZ'))
    return joined_sorted_entries
