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
import time


# If modifying these scopes, delete the file token.pickle.
#https://docs.google.com/spreadsheets/d/1EaSqU0HgAykgIr1se49t6_xwaHoA3kB8ex84781h-io/edit?usp=sharing
# https://docs.google.com/spreadsheets/d/1Gyw5THssc8FqCSqXqni8FHp1_pLjmMHDa6m3Ba501Yk/edit?usp=sharing
# https://docs.google.com/spreadsheets/d/19U9hMr995HcNIUYL0ij8xRn37xz2yZxI_uasQFDizRM/edit?usp=sharing
# https://docs.google.com/spreadsheets/d/1XawJviNBBUJdoMmepxbZKG9Coa0yaVEfDl2xb8TIPEI/edit?usp=sharing
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1EaSqU0HgAykgIr1se49t6_xwaHoA3kB8ex84781h-io' #sandeep.dev.511@gmail.com
SAMPLE_SPREADSHEET_ID = '1_r4da-8nTEwpOLs64dIksoD9xZEiLCFfucidEf70P8g' #chsandeep511@gmail.com

searchDomain_ = []
contactURLs = []
impressumURLs = []
aboutURLs = []
instaURLs = []
overQuota = []

scraped = set()
program_starts = time.time()

#this calss to find the Domain Email List and Contact US emails

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
    read_range_ = 'Sheet31!A2:AA401' #Should be same Row number at line 60: Here I am reading at Column 'A' 10th Row to 20th row

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=read_range_).execute()
    values = result.get('values', [])
    return values


#update Domain Email List URLS =-> Cell K -->Site Emails
def updateToSheetsWithEmails(sheet):

    #TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    range_ = 'Sheet31!K2:AA401' #Should be same Row number at line 50: Here I am updating at Column 'J' 10th Row to 20th row

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

    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    print(response)


#update Contact URLS
def updateToSheetsWithContactUsUrls(sheet):

    #TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    range_ = 'Sheet31!L2:AA401' #Should be same Row number at line 50: Here I am updating at Column 'J' 10th Row to 20th row

    print("*********************************************************************************************************")
    print("ఇది షీట్‌లకు నవీకరించబడుతుంది")
    print('updating to Sheets: %s' % (range_))
    print()

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    value_range_body = {
        #For output, if the spreadsheet data is: A1=1,B1=2,A2=3,B2=4, then requesting range=A1:B2,majorDimension=ROWS will return [[1,2],[3,4]],
        # whereas requesting range=A1:B2,majorDimension=COLUMNS will return [[1,3],[2,4]].
        'values': [contactURLs],
        "majorDimension": "COLUMNS"
    }

    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    print(response)

def updateToSheetsWithAboutUsUrls(sheet):

    #TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    range_ = 'Sheet31!N2:AA401' #Should be same Row number at line 50: Here I am updating at Column 'J' 10th Row to 20th row

    print("*********************************************************************************************************")
    print("ఇది షీట్‌లకు నవీకరించబడుతుంది")
    print('updating to Sheets: %s' % (range_))
    print()

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    value_range_body = {
        #For output, if the spreadsheet data is: A1=1,B1=2,A2=3,B2=4, then requesting range=A1:B2,majorDimension=ROWS will return [[1,2],[3,4]],
        # whereas requesting range=A1:B2,majorDimension=COLUMNS will return [[1,3],[2,4]].
        'values': [aboutURLs],
        "majorDimension": "COLUMNS"
    }

    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    print(response)

def updateToSheetsWithImpreesumUrls(sheet):

    #TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    range_ = 'Sheet31!P2:AA401' #Should be same Row number at line 50: Here I am updating at Column 'J' 10th Row to 20th row

    print("*********************************************************************************************************")
    print("ఇది షీట్‌లకు నవీకరించబడుతుంది")
    print('updating to Sheets: %s' % (range_))
    print()

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    value_range_body = {
        #For output, if the spreadsheet data is: A1=1,B1=2,A2=3,B2=4, then requesting range=A1:B2,majorDimension=ROWS will return [[1,2],[3,4]],
        # whereas requesting range=A1:B2,majorDimension=COLUMNS will return [[1,3],[2,4]].
        'values': [impressumURLs],
        "majorDimension": "COLUMNS"
    }

    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    print(response)


def updateToSheetsWithInstagramUrls(sheet):

    #TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    range_ = 'Sheet31!T2:AA401' #Should be same Row number at line 50: Here I am updating at Column 'J' 10th Row to 20th row

    print("*********************************************************************************************************")
    print("ఇది షీట్‌లకు నవీకరించబడుతుంది")
    print('updating to Sheets: %s' % (range_))
    print()

    # How the input data should be interpreted.
    value_input_option = 'USER_ENTERED'

    value_range_body = {
        #For output, if the spreadsheet data is: A1=1,B1=2,A2=3,B2=4, then requesting range=A1:B2,majorDimension=ROWS will return [[1,2],[3,4]],
        # whereas requesting range=A1:B2,majorDimension=COLUMNS will return [[1,3],[2,4]].
        'values': [instaURLs],
        "majorDimension": "COLUMNS"
    }

    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()
    print(response)


def valid_email(email):
  return bool(re.search(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", email))#r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$


def get_phone(soup):
    try:
        phone = soup.select("a[href*=callto]")[0].text
        return phone
    except:
        pass

    try:
        phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-][2-9][0-9]{2}[-][0-9]{4}\b', response.text)[0]
        return phone
    except:
        pass

    try:
       phone = re.findall(r'\(?\b[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b', response.text)[-1]
       return phone
    except:
        print ('Phone number not found')
        phone = ''
        return phone


def getContactUs(unscraped):
    emails = set()
    while len(unscraped):
        url = unscraped.popleft()
        scraped.add(url)

        parts = urlsplit(url)

        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
          path = url[:url.rfind('/')+1]
        else:
          path = url


        try:
            #print("try")
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US;)'}, timeout=10, allow_redirects=True)# 10 seconds
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.InvalidURL):
            print("except")
            overQuota.append("Error")
            contactURLs.append("Error")
            impressumURLs.append("Error")
            aboutURLs.append("Error")
            instaURLs.append("Error")
            continue

        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+", response.text, re.I)) # should not allow duplicates so using Set
        emails.update(new_emails)

        overQuota.append(str(list(emails)))
        print(str(list(emails)))


        soup = BeautifulSoup(response.text, 'lxml')
        contact_link = ""
        impressum_link = ""
        about_link = ""
        insta_link = ""
        links = []


        for anchor in soup.find_all("a"):
          #print(anchor)
          # extract linked url from the anchor
          # Look for Contact US Page or Imprussm or Instagram or About
          if "href" in anchor.attrs:
            link = anchor.attrs["href"]

            if (('Kontakt' in anchor) or link.find('contatti') != -1) or (link.find('contact') != -1) or (link.find('contattaci') != -1) or (link.find('contattami') != -1) or (link.find('KONTAKT') != -1) or (link.find('kontakt') != -1) or (link.find('KONTAKTY') != -1) or (link.find('Kontakt') != -1) or (link.find('kontakty') != -1) or (link.find('YHTEYDENOTTO') != -1) or (link.find('Yhteystiedot') != -1) or (link.find('yhteystiedot') != -1):
                # resolve relative links (starting with /)
                if link.startswith('/'):
                    link = base_url + link
                    print("if found %s" % link)
                elif link.startswith('http'):
                    print("http found %s" % link)
                else:
                    link = base_url + '/' + link
                    print("else found %s" % link)

                contact_link = link
                continue

            if (link.find('IMPRESSUM') != -1) or (link.find('impressum') != -1) or (link.find('Impressum') != -1):
                if link.startswith('/'):
                    link = base_url + link
                    print("if found %s" % link)
                elif link.startswith('http'):
                    print("http found %s" % link)
                else:
                    link = base_url + '/' + link
                    print("else found %s" % link)

                impressum_link = link
                continue

            if ((link.find('About') != -1) or (link.find('about') != -1)):
                if link.startswith('/'):
                    link = base_url + link
                elif link.startswith('http'):
                    print("http found %s" % link)
                else:
                    link = base_url + '/' + link
                    print("else found %s" % link)

                about_link = link
                continue

            if ((link.find('instagram') != -1) or (link.find('Instagram') != -1)):
                if link.startswith('/'):
                    link = base_url + link
                elif link.startswith('http'):
                    print("http found %s" % link)
                else:
                    link = base_url + '/' + link
                    print("else found %s" % link)

                insta_link = link
                continue

          else:
            #print(" else - not an href")
            link = ''
            # resolve relative links (starting with /)
            if link.startswith('/'):
                link = base_url + link

            elif not link.startswith('http'):
                link = path + link

            if not link.endswith(".gz"):
              if not link in unscraped and not link in scraped:
                  unscraped.append(link)

            if (('Kontakt' in anchor) or link.find('contatti') != -1) or (link.find('contact') != -1) or (link.find('contattaci') != -1) or (link.find('contattami') != -1) or (link.find('KONTAKT') != -1) or (link.find('kontakt') != -1) or (link.find('KONTAKTY') != -1) or (link.find('Kontakt') != -1) or (link.find('kontakty') != -1) or (link.find('Yhteystiedot') != -1) or (link.find('yhteystiedot') != -1) or (link.find('YHTEYDENOTTO') != -1):
                print(link)
                contact_link = link
                print("else block 193")

            if (link.find('IMPRESSUM') != -1) or (link.find('impressum') != -1) or (link.find('Impressum') != -1):
                print(link)
                impressum_link = link
                print("else block 193")

            if ((link.find('instagram') != -1) or (link.find('Instagram') != -1)):
                print(link)
                insta_link = link
                print("else block 193")

            if ((link.find('About') != -1) or (link.find('about') != -1)):
                print(link)
                about_link = link
                print("else block 193")

        contactURLs.append(contact_link)
        impressumURLs.append(impressum_link)
        aboutURLs.append(about_link)
        instaURLs.append(insta_link)


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
                #searchDomain_.append(row[0])

    count = 1

    for original_url in searchDomain_:
        now = time.time()

        print('{0}'.format(count) + ", Crawling URL %s" % original_url)
        count = count + 1

        if not original_url:#if URL is empty like []
            overQuota.append(str(original_url))
            contactURLs.append(str(original_url))
            impressumURLs.append(str(original_url))
            aboutURLs.append(str(original_url))
            instaURLs.append(str(original_url))
        else:
            unscraped = deque([original_url])
            getContactUs(unscraped)


    updateToSheetsWithEmails(sheet)
    updateToSheetsWithContactUsUrls(sheet)
    updateToSheetsWithImpreesumUrls(sheet)
    updateToSheetsWithAboutUsUrls(sheet)
    updateToSheetsWithInstagramUrls(sheet)

    print("It has been {0} seconds since the loop started".format(now - program_starts))

if __name__ == '__main__':
    main()
