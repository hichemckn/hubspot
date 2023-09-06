import hubspot
from pprint import pprint
from hubspot.crm.companies import BatchInputSimplePublicObjectInputForCreate, ApiException

API_KEY = '******'

client = hubspot.Client.create(access_token=API_KEY)

batch_input_simple_public_object_input_for_create =   \
                BatchInputSimplePublicObjectInputForCreate(inputs=[
                                                                    {"properties":{"city":"Cambridge",
                                                                                "domain":"biglytics0111.net",
                                                                                "industry":"Technology",
                                                                                "name":"Biglytics011",
                                                                                "phone":"(877) 929-0687",
                                                                                "state":"Massachusetts",
                                                                                "k_alphaplan_addressenid_hubspot":"6771"},
                                                                    },
                                                                    {"properties":{"city":"Cambridge",
                                                                                "domain":"biglytics0112.net",
                                                                                "industry":"Technology",
                                                                                "name":"Biglytics0112",
                                                                                "phone":"(877) 929-0687",
                                                                                "state":"Massachusetts",
                                                                                "k_alphaplan_addressenid_hubspot":"7771"
                                                                                
                                                                                },
                                                                    }
                                                                ]
                                                            )
try:
    api_response = client.crm.companies.batch_api.create(batch_input_simple_public_object_input_for_create=batch_input_simple_public_object_input_for_create)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling batch_api->create: %s\n" % e)
