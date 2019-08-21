#!/usr/bin/python3
#
# Usage: test-sheet.py 
# 

import sys
import re
import csv

import json
import gspread
#from oauth2client.client import SignedJwtAssertionCredentials

import httplib2

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

CLIENT_SECRET = 'google/andresillo.json'
SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
STORAGE = Storage('credentials.storage')

# Start the OAuth flow to retrieve credentials
def authorize_credentials():
# Fetch credentials from storage
    credentials = STORAGE.get()
# If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials


def main():
  json_key = json.load(open("google/andresillo.json"))

  scope = ['https://spreadsheets.google.com/feeds']


  #credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
  credentials = credentials = authorize_credentials()
  gc = gspread.authorize(credentials)
  # =IMPORTHTML("http://basketball.realgm.com/nba/stats/2016/Averages/All/player/All/desc/1/Regular_Season","table",1)
  worksheet = gc.open("andresillo").sheet1
  with open("players.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(worksheet.get_all_values())

  # =IMPORTHTML("http://basketball.realgm.com/nba/schedules","table",0)
  worksheet = gc.open("lista igraca").get_worksheet(3)
  with open("games.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(worksheet.get_all_values())

if __name__ == '__main__':
  main()
