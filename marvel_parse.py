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



def main():
    json_data = getCharacterData(1009368)
    results = json_data["data"]["results"][0]
    name = results["name"]
    description = results["description"]
    img_path = results["thumbnail"]["path"] + "." + results["thumbnail"]["extension"]

    print("Name = %s\nDescription = %s\nimg path = %s" %(name, description, img_path))
 
if __name__ == "__main__":
    main()   

