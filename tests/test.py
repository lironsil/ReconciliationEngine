import requests
import json

def send_request():
   payments = json.load(open('payments.json'))
   headers = {'Content-Type': 'application/json'}
   request = requests.post('http://127.0.0.1:5000/', json=payments, headers=headers)
   if request.status_code == 200:
     return request.json()
   else:
     raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, "query error"))

transactions=send_request()
for keys,values in transactions.items():
    print(keys)
    print(values)