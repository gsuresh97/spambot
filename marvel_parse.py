#!/usr/bin/python

import json
import requests
import hashlib
import time
import random

apiKey = "a116c36fab7472b082b231386809a3cc";
privateKey = "cf264aec6c9964ba8b5bb55929f55a9bfe1bf3f0";
id_arr = [1009368, 1009351, 1009610, 1009547]


def hashFunction(time):
    preHash = str(time) + privateKey + apiKey
    m = hashlib.md5(preHash)
    return m.hexdigest()

def getCharacterData(characterID):
    # get current systime
    ts = int(time.time())

    url = "http://gateway.marvel.com/v1/public/characters/"+ str(characterID)
    parameters = {"ts" : ts, 
                  "apikey" : apiKey, 
                  "hash" : hashFunction(ts)}
    resp = requests.get(url=url, params=parameters)
    data = json.loads(resp.text)
    return data

# this is the function to call
def getMarvelData():
    
    rand = int(random.random()*len(id_arr))
    
    json_data = getCharacterData(id_arr[rand])
    results = json_data["data"]["results"][0]
    name = results["name"]
    description = results["description"]
    img_path = results["thumbnail"]["path"] + "." + results["thumbnail"]["extension"]
    
    return (name, description, img_path)

def emailFormat():
    name, description, img_path = getMarvelData()
    print(name)
    out = "Hello:\n\n It is with great pleasure that I present you with a very important task.\nShould you choose to accept this mission, you will find the below information of great interest to you:\n\n"
    n = 0
#    for letter in s:
#        out += letter
#        if letter == '\n':
#            n+=1
#            out += '\n'
#        if n == 2:
#            out += "Below I have opened my Western Union account. Please forward the funds here. Good luck, and may Thor be with you.\n\n"
#            n+=1                
    return out    


print(emailFormat())
