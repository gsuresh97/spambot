import sys
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
