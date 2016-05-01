#!/usr/bin/python

import json
import requests
import hashlib
import time

apiKey = "a116c36fab7472b082b231386809a3cc";
privateKey = "cf264aec6c9964ba8b5bb55929f55a9bfe1bf3f0";
#id_arr = [1009368, 


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
    json_data = getCharacterData(1009368)
    results = json_data["data"]["results"][0]
    name = results["name"]
    description = results["description"]
    img_path = results["thumbnail"]["path"] + "." + results["thumbnail"]["extension"]

    return "Name = %s\nDescription = %s\nimg path = %s" %(name, description, img_path)

def emailFormat():
    s = getMarvelData()
    out = "Hello:\nShould you choose to accept this mission, you will find the below information of great interest.\n"
    n = 0
    for letter in s:
        out += letter
        if letter == '\n':
            n+=1
        if n == 2:
            out += "Below I have opened my Western Union account. Please forward the funds here. Good luck, and may Thor be with you.\n"
            continue
    return out    


print(emailFormat())
