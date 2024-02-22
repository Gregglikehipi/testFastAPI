import requests
import json

def api_get(id):
    r = requests.get(f'http://api:80/get/{id}')
    response = json.loads(r.text)
    return response

def api_add(id):
    r = requests.post(f'http://api:80/add/{id}')
    response = json.loads(r.text)
    return response

def api_get_all():
    r = requests.get('http://api:80/get_all/')
    response = json.loads(r.text)
    return response

def api_delete(id):
    r = requests.delete(f'http://api:80/delete/{id}')
    response = json.loads(r.text)
    return response

def api_priceHistory(id):
    r = requests.get(f'http://api:80/historyPrice/{id}')
    response = json.loads(r.text)
    return response

def api_countGroup(id):
    r = requests.get(f'http://api:80/countGroup/{id}')
    response = json.loads(r.text)
    return response

def api_countAll():
    r = requests.get(f'http://api:80/countAll')
    response = json.loads(r.text)
    return response

def api_average(id):
    r = requests.get(f'http://api:80/comparePrice/{id}')
    response = json.loads(r.text)
    return response
