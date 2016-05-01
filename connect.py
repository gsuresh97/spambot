import sys
import imaplib
import email
import email.header
import datetime

import json
import requests
import hashlib
import time
import random
from random import shuffle

import smtplib

EMAIL_ACCOUNT = "johndoe3451@yahoo.com"
EMAIL_FOLDER = "Bulk Mail"

apiKey = "a116c36fab7472b082b231386809a3cc";
privateKey = "cf264aec6c9964ba8b5bb55929f55a9bfe1bf3f0";
id_arr = [1009368, 1009351, 1009610, 1009547, 1009220, 1009664, 1009629, 1009356, 1009366, 1009662, 1009175, 1009257, 1009310, 1009313, 1009362, 1009496, 1009381, 1009508, 1009472, 1009476, 1009512, 1009546, 1009718, 1009722, 1010735, 1010763, 1010743, 1010744]


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

def pickKeyWords(key_phrases, name):
    phrases = []
    rand1 = random.random() * len(key_phrases)
    rand2 = random.random() * len(key_phrases)
    
    for i in range(len(key_phrases)):
        if name in key_phrases[i]:
            continue
        if (len(key_phrases[i].split(' ')) > 1):
            phrases.append(key_phrases[i])
        elif(i == rand1 or i == rand2):
            phrases.append(key_phrases[i])

    question = "Which Marvel superhero is most personified as being associated to "
    shuffle(phrases)
    for i in range(len(phrases)):
        question += phrases[i]
        if (i < len(phrases)-1):
            question += ", "
        if (i == len(phrases)-2):
            question += "and "

    question += "?"
    return question
            
def q1(description, name):
    azureKey = "82e9a92b30e442e0bc0cc202969a1656"
    headrs = {'content-type':'application/json', "ocp-apim-subscription-key": azureKey }
    parameters = {"documents": 
                  [{"language": "en",
                     "id" : "string", 
                     "text" : description 
                     }]
                  }
    
    url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases"
    resp = requests.post(url, data = json.dumps(parameters), headers=headrs)
    data = json.loads(resp.text)
    all_key_phrases = data['documents'][0]["keyPhrases"]
    question = pickKeyWords(all_key_phrases, name)
    
    return question

def emailFormat():
    name, description, img_path = getMarvelData()

    # to ensure that there is a description for the superhero
    while (description == "" or name == ""):
        name, description, img_path = getMarvelData()

    base = "Hello:\n\nI am intruigued by your offer. However, before I can help you, I must ask you a very important question:\n\n"
    msg = base

    question = q1(description, name)

    return msg + question + "\n"



def process_mailbox(M):    
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return

    N = smtplib.SMTP('smtp.gmail.com')
    N.ehlo
    N.starttls()
    N.login('johndoe52541@gmail.com' , 'jiminycricket')

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        #rv, data = M.store(num,'-FLAGS','\\Seen')
        if rv != 'OK':
            print "ERROR getting message", num
            return
        
        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        print 'Message %s: %s' % (num, subject)
        print 'Raw Date:', msg['Date']
        sender = msg['From']
        if sender:
            msgb = "\r\n".join([
                "From: johndoe52541@gmail.com",
                "To: " + sender,
                "Subject: Have you heard the good news?",
                "",
                emailFormat()
            ])
            N.sendmail('johndoe52541@gmail.com', sender, msgb)
        
            # Now convert to local date-time
            date_tuple = email.utils.parsedate_tz(msg['Date'])
            if date_tuple:
                local_date = datetime.datetime.fromtimestamp(
                    email.utils.mktime_tz(date_tuple))
                print "Local Date:", \
                    local_date.strftime("%a, %d %b %Y %H:%M:%S")
    N.logout()

            
M = imaplib.IMAP4_SSL('imap.mail.yahoo.com')

try:
    rv, data = M.login(EMAIL_ACCOUNT, 'jiminycricket')
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    sys.exit(1)
    
print rv, data
    
rv, mailboxes = M.list()
if rv == 'OK':
    print "Mailboxes:"
    print mailboxes
        
rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print "Processing mailbox...\n"
    process_mailbox(M)
    M.close()
else:
    print "ERROR: Unable to open mailbox ", rv    

    M.logout()
