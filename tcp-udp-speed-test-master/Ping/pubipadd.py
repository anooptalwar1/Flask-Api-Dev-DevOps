import requests

pubip_url = "http://www.ip-api.com/json"
api_call = requests.get(pubip_url)
data = api_call.json()
ip = data['query']
print (ip)
