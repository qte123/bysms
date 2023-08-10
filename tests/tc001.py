import requests, pprint
from django.core.serializers.json import json

payload = {
    'username': 'byhy',
    'password': '12345678'
}

response = requests.post('http://localhost:8000/api/mgr/signin/', data=payload)

pprint.pprint(response.text)
