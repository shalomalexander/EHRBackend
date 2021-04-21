import smtplib

li = []
account = ""
password = ""
f = open("demofile.txt", "r")
for x in f:    
  li.append(x)

account = str(li[0])
password = str(li[1])

sender = '1709510038@coet.in'
receivers = ['dhoundiyals19@gmail.com']

message = """From: From Person <shalomalexander68@gmail.com>
To: To Person <dhoundiyals19@gmail.com>
Subject: SMTP e-mail test

YE SUNITA BDI VO HE
"""

try:
   smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
   smtpObj.ehlo()
   smtpObj.starttls()
   smtpObj.login(account, password)
   smtpObj.sendmail(sender, receivers, message)         
   print("Successfully sent email") 
except smtplib.SMTPException:
   print("Error: unable to send email") 