# -*- coding: utf-8 -*-
"""API Practice 4

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vwNd6UNbNYAJf9AxRTRk0Rp8maSDdzY0
"""

import requests
import json

api_key='x4NrrrA_btSd38iHB79GetIAcPlsF-e-VCtCdlYR7z7lzqlGFhlvmZBNkhktY_kq1nDHoiJSJZoW9YUf1WXvmmo4VDIbiwN7P2fG4cpIUCeWSGhZF31AS9CWPfCqXnYx'
url='https://api.yelp.com/v3/businesses/search'
headers={'Authorization':'Bearer %s'% api_key}
params={'term':'bookstore','location':'Raleigh'}

#Making a get request to the API

req=requests.get(url,params=params,headers=headers)
parsed=json.loads(req.text)
#print(json.dumps(parsed,indent=4))

#To Check status code
print('The status code is {}'.format(req.status_code))

#json.loads(req.text)

businesses=parsed["businesses"]
for businesses in businesses:
    if(businesses["rating"]>=4.5):
        print("Name :",businesses["name"])
        print("Rating:",businesses["rating"])
        print("Location:".join(businesses['location']['display_address']))
        print("Phone :",businesses["phone"])
        print("\n")

        id=businesses["id"]        

        url="https://api.yelp.com/v3/businesses/"+id+"/reviews"
        req=requests.get(url,headers=headers)
        parsed=json.loads(req.text)
        print(json.dumps(parsed,indent=4))

import requests
import json

api_key='x4NrrrA_btSd38iHB79GetIAcPlsF-e-VCtCdlYR7z7lzqlGFhlvmZBNkhktY_kq1nDHoiJSJZoW9YUf1WXvmmo4VDIbiwN7P2fG4cpIUCeWSGhZF31AS9CWPfCqXnYx'
url='https://api.yelp.com/v3/businesses/search'
headers={'Authorization':'Bearer %s'% api_key}
params={'term':'book store','location':'Raleigh'}

#Making a get request to the API

req=requests.get(url,params=params,headers=headers)
parsed=json.loads(req.text)
print(parsed)

businesses=parsed["businesses"]
for business in businesses:
    id=business["id"]
    url="https://api.yelp.com/v3/businesses/"+ id +"/reviews"
    req=requests.get(url,headers=headers)
    parsed=json.loads(req.text)
    reviews=parsed["reviews"]
    for review in reviews:
        print("Name : ",review["user"]["name"]," Rating : ",review["rating"],"Review :",review["text"],"\n")


 


#To Check status code
print('The status code is {}'.format(req.status_code))