from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import json
import re
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
from google.colab import files


# If modifying these scopes, delete the file token.pickle.
#https://docs.google.com/spreadsheets/d/1EaSqU0HgAykgIr1se49t6_xwaHoA3kB8ex84781h-io/edit?usp=sharing
# https://docs.google.com/spreadsheets/d/1Gyw5THssc8FqCSqXqni8FHp1_pLjmMHDa6m3Ba501Yk/edit?usp=sharing
# https://docs.google.com/spreadsheets/d/19U9hMr995HcNIUYL0ij8xRn37xz2yZxI_uasQFDizRM/edit?usp=sharing
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1EaSqU0HgAykgIr1se49t6_xwaHoA3kB8ex84781h-io' #sandeep.dev.511@gmail.com
SAMPLE_SPREADSHEET_ID = '1meboQWv-2OMnM328b2BGGseG9bUcR6KZ9PeMTgVBMI0' #chsandeep511@gmail.com

searchDomain_ = []
overQuota = []
scraped = set()

#emails = set()

def initializeSheets():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    return sheet


def readSheets(sheet):
    #TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    # The A1 notation of the values to update.
    # start with A2 always
    read_range_ = 'Sheet2!A2:AA101' #Should be same Row number at line 60: Here I am reading at Column 'A' 10th Row to 20th row

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=read_range_).execute()
    values = result.get('values', [])
    return values


def updateToSheets(sheet):

    #TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    range_ = 'Sheet2!K2:AA101' #Should be same Row number at line 50: Here I am updating at Column 'J' 10th Row to 20th row

    print("*********************************************************************************************************")
    print("ఇది షీట్‌లకు నవీకరించబడుతుంది")
    print('updating to Sheets: %s' % (range_))
    print()

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    value_range_body = {
        #For output, if the spreadsheet data is: A1=1,B1=2,A2=3,B2=4, then requesting range=A1:B2,majorDimension=ROWS will return [[1,2],[3,4]],
        # whereas requesting range=A1:B2,majorDimension=COLUMNS will return [[1,3],[2,4]].
        'values': [overQuota],
        "majorDimension": "COLUMNS"
    }

    #print(overQuota)
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    print(response)


def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


def fetchEmailList(unscraped):
    emails = set()
    while len(unscraped):
        #print(unscraped)
        url = unscraped.popleft()
        scraped.add(url)

        parts = urlsplit(url)

        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
          path = url[:url.rfind('/')+1]
        else:
          path = url

        print("Crawling URL %s" % url)

        try:
            #print("try")
            response = requests.get(url, timeout=10)# 10 seconds
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("except")
            overQuota.append("Error")
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+", response.text, re.I)) # should not allow duplicates so using Set

        emails.update(new_emails)
        overQuota.append(str(list(emails)))


        soup = BeautifulSoup(response.text, 'lxml')

        for anchor in soup.find_all("a"):
          if "href" in anchor.attrs:
              link = anchor.attrs["href"]

          else:
            link = ''
            if link.startswith('/'):
                link = base_url + link

            elif not link.startswith('http'):
                link = path + link

            if not link.endswith(".gz"):
              if not link in unscraped and not link in scraped:
                  unscraped.append(link)

    print(emails)
    #overQuota.append(str(emails))

def main():
    # [START sheets_get_values]
    sheet = initializeSheets()
    values = readSheets(sheet)
    print('{0} rows retrieved.'.format(len(values)))
    # [END sheets_get_values]

    if not values:
        print('No data found.')
        return
    else:
        #print(values)
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('%s, %s' % (row[0], row[1]))
            #print(row[0]) == Domain
            if not row:
                print("List is empty")
                searchDomain_.append(row)
            else:
                #print("List is not empty")
                searchDomain_.append('http://'+row[0])

    #print(searchDomain_)
    for original_url in searchDomain_:
        if not original_url:
            overQuota.append(str(original_url))
        else:
            unscraped = deque([original_url])
            fetchEmailList(unscraped)

        #print(emails)
        #overQuota.append(str(emails))

    print(overQuota)

    #updateToSheets(sheet)


if __name__ == '__main__':
    main()
