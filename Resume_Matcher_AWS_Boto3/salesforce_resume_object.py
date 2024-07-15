import requests
import json

# def lambda_handler(event, context):
#     # Salesforce API authentication
#     auth_url = 'https://login.salesforce.com/services/oauth2/token'
#     payload = {
#         'grant_type': 'password',
#         'client_id': '3MVG9GCMQoQ6rpzQmNu7bIXl8of9ZZ_t2EQz5tk5sRT0IABYF1tVfYqffero4o52Y.kCBOySSirPtosNZWL4f',
#         'client_secret': 'EB1EEB5CF6E21E7A536D9E70FF7798E25A547193F0F3E3D30CF8F6C05A3798F7',
#         'username': 'raushan9jnv@gmail.com',
#         'password': 'Robin@959GwpUNGgUnZOL1hKGwABWFeNDp'
#     }
#     response = requests.post(auth_url, data=payload)
#     access_token = response.json()['access_token']

#     # Salesforce API request to query Resume data
#     api_url = 'https://ddl000000s9q9uak-dev-ed.develop.my.salesforce.com/services/data/v60.0/query/?q=SELECT+Resume_ID__c,Resume_Link__c,Job_Description__c+FROM+Resume__c'
#     headers = {
#         'Authorization': 'Bearer ' + access_token,
#         'Content-Type': 'application/json'
#     }
#     response = requests.get(api_url, headers=headers)
#     # print(response)
#     data = response.json()['records']
#     # print(data)

#     # Process data as needed
#     for record in data:
#         resume_id = record['resume_id__c']
#         print(resume_id)
#         resume_link = record['resume_link__c']
#         print(resume_link)
#         job_description = record['job_description__c']
        
#         # Perform further processing or return the data

#     return {
#         'statusCode': 200,
#         'body': json.dumps('Data retrieved from Salesforce')
#     }

auth_url = 'https://login.salesforce.com/services/oauth2/token'
payload = {
        'grant_type': 'password',
        'client_id': '3MVG9GCMQoQ6rpzQmNu7bIXl8of9ZZ_t2EQz5tk5sRT0IABYF1tVfYqffero4o52Y.kCBOySSirPtosNZWL4f',
        'client_secret': 'EB1EEB5CF6E21E7A536D9E70FF7798E25A547193F0F3E3D30CF8F6C05A3798F7',
        'username': 'raushan9jnv@gmail.com',
        'password': 'Robin@959GwpUNGgUnZOL1hKGwABWFeNDp'
    }
response = requests.post(auth_url, data=payload)
access_token = response.json()['access_token']

    # Salesforce API request to query Resume data
api_url = 'https://ddl000000s9q9uak-dev-ed.develop.my.salesforce.com/services/data/v60.0/query/?q=SELECT+Resume_ID__c,Resume_Link__c,Job_Description__c+FROM+Resume__c'
headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
response = requests.get(api_url, headers=headers)
    # print(response)
data = response.json()['records']
    # print(data)

    # Process data as needed
for record in data:
    resume_id = record['resume_id__c']
    print(resume_id)
    resume_link = record['resume_link__c']
    print(resume_link)
    job_description = record['job_description__c']
