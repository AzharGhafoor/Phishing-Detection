from imaplib import IMAP4_SSL
import email as em
from email.utils import parsedate, parsedate_tz
from email.parser import HeaderParser
import numpy as np
import pandas as pd
import getpass
from datetime import timedelta, datetime, date


class OutlookAccount(object):
    def __init__(self, username=None, password=None, folder=None):
        self.username = username
        self.password = password
        self.folder = folder

    def login(self):
        self.conn = IMAP4_SSL('outlook.office365.com')
        response = self.conn.login(self.username, self.password)
        return response

    def search(self, query, folder=None, readonly=False):
        ff = self.folder if self.folder else folder
        self.conn.select(ff, readonly)
        resp, data = self.conn.search(None, query)
        return data

    def fetch(self, uids, query):
        uid_arr = b','.join(uids[0].split())
        resp, data = self.conn.fetch(uid_arr, query)
        return data

    def fetch_and_parse(self, uids, query):
        data = self.fetch(uids, query)
        parser = HeaderParser()
        emails = []

        for email in data:
            if len(email) < 2:
                continue
            msg = em.message_from_bytes(email[1]).as_string()
            emails.append(parser.parsestr(msg))

        return emails

    def load_parse_query(self, search_query, fetch_query, folder=None, readonly=False):
        uids = self.search(search_query, folder, readonly)
        return self.fetch_and_parse(uids, fetch_query)

#imap_password = 'YourEmailPassword'
#imap_username = 'yourOutlookMail@outlook.com'

imap_password = '5F18978'
imap_username = 'fa20-ris-003@isbstudent.comsats.edu.pk'
 
outlook = OutlookAccount(username=imap_username, password=imap_password)
outlook.login()

daysback = 6000 # ~10yrs...make this whatever ya like
notsince = 0 # since now.
since = (date.today() - timedelta(daysback)).strftime("%d-%b-%Y")
before = (date.today() - timedelta(notsince)).strftime("%d-%b-%Y")

SEARCH = '(SENTSINCE {si} SENTBEFORE {bf})'.format(si=since, bf=before)
ALL_HEADERS = '(BODY.PEEK[HEADER])'

# Search and fetch emails!
received = outlook.load_parse_query(search_query=SEARCH, fetch_query=ALL_HEADERS, folder='"INBOX"')


#create function to convert to dataframe
def scrub_email(headers):   
    return dict([(title.lower(), value) for title, value in headers]) 

df = pd.DataFrame([scrub_email(email._headers) for email in received])


#copy of df, not necessary but in case if you have to make changes in dataframe, we will also have the old one
df2 = df


#approach-1
import re
mail_re = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

traversed_index = []

fake_mail = df2['x-sender-id'].values
sender = df2['from'].values

for i,(m, n) in enumerate(zip(fake_mail,sender)):

    fk_email = re.findall(mail_re, str(m))
    sdr_email = re.findall(mail_re, str(n))
    if(len(fk_email)>0):
        if(fk_email != sdr_email):
            traversed_index.append(i)
            domain = fk_email[0][fk_email[0].index('@') + 1 : ]
            print("+ \t It could be Phishing")
            x_mail_df = df2.iloc[i]
            a = x_mail_df['x-mailer']
            if(len(a)>0):
                print("Sender: "+a)
            else:
                print("Sender: "+domain)
            print("Sent From: https://"+str(domain))
            print("Origional Sender: ",fk_email)
            print("Pretender Sender: ",sdr_email,"\n\n")
			

#approach-2
import re
mail_re = r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+"

traversed_index1 = []
ph_vals = df2['message-id'].values
sender = df2['from'].values

for i,(m, n) in enumerate(zip(ph_vals,sender)):
    
    ph_email = re.findall(mail_re, str(m))
    sdr_email = re.findall(mail_re, str(n))
    
    if(len(ph_email)>0):
        if(ph_email != sdr_email):
            traversed_index1.append(i)
            domain = ph_email[0][ph_email[0].index('@') + 1 : ]
            print("Sent From: https://"+str(domain))
            print("Origional Sender: ",ph_email)
            print("Pretender Sender: ",sdr_email,"\n\n")