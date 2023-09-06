import requests
import json
from credentials import API_KEY

# Set up the API endpoint URL
url = 'https://api.hubapi.com/contacts/v1/contact/batch/'

# Set up your HubSpot API key
api_key = API_KEY

# Set up the contact data to be uploaded
contact_data = [
                    {
                    "email":"hichem1204@qurix.tech",
                    "properties": [
                                    
                                    {
                                        "property": "email",
                                        "value": "hichem1204@qurix.tech"
                                    },
                                    {
                                        "property": "firstname",
                                        "value": "hichem1204-1"
                                    },
                                    {
                                        "property": "lastname",
                                        "value": "chakroun1204"
                                    },
                                    {
                                        "property": "phone",
                                        "value": "+49176744823992"
                                    },
                                    {
                                        "property": "adressgruppe",
                                        "value": "1204"
                                    },
                                    {
                                        "property": "suchname",
                                        "value": "hichemch1204"
                                    }                                
                                    ]
                    },
                    {
                    "email":"hichem1205@qurix.tech",
                    "properties":[
                                    {
                                        "property": "email",
                                        "value": "hichem1205@qurix.tech"
                                    },                                    
                                    {
                                        "property": "firstname",
                                        "value": "hichem1205"
                                    },
                                    {
                                        "property": "lastname",
                                        "value": "chakroun1205-1"
                                    },
                                    {
                                        "property": "phone",
                                        "value": "+49176744823992"
                                    },
                                    {
                                        "property": "adressgruppe",
                                        "value": "1205"
                                    },
                                    {
                                        "property": "suchname",
                                        "value": "hichemch1205"
                                    }                               
                                    ]
                    },
                    {
                    "email":"hichem1206@qurix.tech",
                    "properties":[
                                    {
                                        "property": "email",
                                        "value": "hichem1206@qurix.tech"
                                    },                                    
                                    {
                                        "property": "firstname",
                                        "value": "hichem1206"
                                    },
                                    {
                                        "property": "lastname",
                                        "value": "chakroun1206"
                                    },
                                    {
                                        "property": "phone",
                                        "value": "+49176744823992"
                                    },
                                    {
                                        "property": "adressgruppe",
                                        "value": "1206"
                                    },
                                    {
                                        "property": "suchname",
                                        "value": "hichemch1206"
                                    }                               
                                    ]
                    }
                ]

# Convert the contact data to JSON format
data = json.dumps(contact_data)

# Set up the request headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_key
}

# Make the API request
response = requests.post(url, headers=headers, data=data)

# Print the response status code and content
if response.status_code == 202:
    print("Contacts were successfully imported to Hubspot.")
elif response.status_code == 409:
    print("Conflict error while imported to Hubspot.")
elif response.status_code == 400:
    print("there is a problem with the data in the request body,there are no properties included in the request data.")    
else:
    print("An error occurred while importing contacts to Hubspot. Status code: ", response.status_code)
