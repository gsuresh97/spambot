import sys
import smtplib
import email
import datetime

M = smtplib.SMTP('smtp.gmail.com')

msg = "\r\n".join([
      "From: johndoe52541@gmail.com",
      "To: johndoe3451@yahoo.com",
      "Subject: Spam",
      "",
      "This is ngrn prnc. pls snd $$ kthxbye"
      ])
M.ehlo
M.starttls()
M.login('johndoe52541@gmail.com' , 'jiminycricket')
for i in range(1, 100):
    msg = "\r\n".join([
      "From: johndoe52541@gmail.com",
      "To: johndoe3451@yahoo.com",
      "Subject: Spam"+str(i),
      "",
      "This is ngrn prnc. pls snd $$ kthxbye"
      ])
    M.sendmail('johndoe52541@gmail.com', 'johndoe3451@yahoo.com', msg)
M.quit()
