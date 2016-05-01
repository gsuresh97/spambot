"""import sys
import imaplib
import email
import datetime

M = imaplib.IMAP4_SSL('imap.mail.yahoo.com')

try:
    M.login("johndoe3451@yahoo.com", "jiminycricket")
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!!"

rv, mailboxes = M.list()
if rv == 'OK':
    print "Mailboxes:"
    print mailboxes


M.select('(\\Junk \\HasNoChildren) "/" "Bulk Mail"')
rv, data = M.search(None, '(\\Junk \\HasNoChildren) "/" "Bulk Mail"')
"""

import sys
import imaplib
import email
import email.header
import datetime

EMAIL_ACCOUNT = "johndoe3451@yahoo.com"
EMAIL_FOLDER = "Bulk Mail"

def process_mailbox(M):    
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return
    
    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        rv, data = M.store(num,'-FLAGS','\\Seen')
        if rv != 'OK':
            print "ERROR getting message", num
            return
        
        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        print 'Message %s: %s' % (num, subject)
        print 'Raw Date:', msg['Date']
        print 'Sender: ', msg['From']
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")
    
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
