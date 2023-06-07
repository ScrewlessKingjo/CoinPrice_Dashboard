import requests
import json
import redis

URL = "https://api.bithumb.com/public/ticker/ALL_KRW"
HEADERS = {"accept": "application/json"}

rd = redis.StrictRedis(host='localhost', port=6379, db=0)

# rd.set('test', 'test1')
data = rd.get('test')

data.type()

def DataGenerator(url, headers) : 

    response = requests.get(url, headers=headers).text
    data = json.loads(response)
    
    return data