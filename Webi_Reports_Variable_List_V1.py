# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 12:49:07 2024

@author: Amey.Satpute
"""

import requests
import pandas as pd
import sys

print('************************************************************************')
print(' Title : Webi Report Variables List \n Author: Amey Vijaykumar Satpute \n Version:1.0')
print('************************************************************************')

#Parameters
ip = sys.argv[1]
userName = sys.argv[2]
password = sys.argv[3]
document_id = sys.argv[4]
logging_path = sys.argv[5]

variablelist = []
variablenames = []

#create a BI session
Login_URL = f'https://{ip}:443/biprws/logon/long'
r = requests.get(url = Login_URL)
request_login_data = {"userName": userName,
                "password": password,
                "auth": "secEnterprise"}
post_login_response = requests.post(url = Login_URL, json=request_login_data)
X_SAP_LogonToken = post_login_response.headers['X-SAP-LogonToken']
headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-SAP-LogonToken': X_SAP_LogonToken}

document_details_url = f'https://{ip}:443/biprws/raylight/v1/documents/{document_id}'
document_details = requests.get(url = document_details_url, headers = headers)
document_name = document_details.json()['document']['name']


document_variable_url = f'https://{ip}:443/biprws/raylight/v1/documents/{document_id}/variables'
variables_list = requests.get(url = document_variable_url, headers = headers)
dict1 = list(variables_list.json().values())[0].values()

for i in pd.DataFrame(dict1).to_numpy()[0]:
    variablelist.append(i['id'])
    variablenames.append(i['name'])
    
for i,j in zip(variablelist, variablenames):
    variable_def_url = f'https://{ip}:443/biprws/raylight/v1/documents/{document_id}/variables/{i}'
    variable_def_request = requests.get(url = variable_def_url, headers = headers)
    variable_def = list(variable_def_request.json().values())
    variable_def_dict = pd.DataFrame(variable_def).to_dict()
    with open (f'{logging_path}\\{document_name}_variables.txt','a') as file:
        file.writelines(j + variable_def_dict['definition'][0] + '\n') 
        file.close()
    