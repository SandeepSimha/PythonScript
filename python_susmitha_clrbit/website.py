from __future__ import print_function
import os
import webbrowser
import ssl
import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
import operator
from google.colab import files

import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException



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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


SAMPLE_SPREADSHEET_ID = '1meboQWv-2OMnM328b2BGGseG9bUcR6KZ9PeMTgVBMI0' #chsandeep511@gmail.com

searchDomain_ = []
overQuota = []
scraped = set()

subDescEmail = set()
senderEmailList_ = []


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
    read_range_ = 'Sheet10!P154:AA155' #Should be same Row number at line 60: Here I am reading at Column 'A' 10th Row to 20th row

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=read_range_).execute()
    values = result.get('values', [])
    return values

def valid_email(email):
  return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

def openChromeDriver(to_, subject_, composebody_):
    chromedriver = "/Users/sancheru/Downloads/chromedriver"

    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")
    driver = webdriver.Chrome(chromedriver)#,options=chrome_options)
    driver.get('https://caprica.seoboxes.com:2096/cpsess8220829249/3rdparty/roundcube/?_task=mail&_action=compose&_id=14557673775fb5a90c1c498')


    username_input = '//*[@id="user"]'
    password_input = '//*[@id="pass"]'
    login_submit = '//*[@id="login_submit"]'
    #driver.find_element_by_xpath(first_login).click()
    driver.find_element_by_xpath(username_input).send_keys("stewardsmike@trafficluxury.com")#stewardsmike@trafficluxury.com
    driver.find_element_by_xpath(password_input).send_keys("stewardsmike34")
    driver.find_element_by_xpath(login_submit).click()
    driver.maximize_window()
    time.sleep(2)
    print("Window has been opened")

    driver.find_element_by_xpath('//*[@id="rcmbtn107"]').click()
    print("Navigating to Next Page")
    time.sleep(1)
    print("Sleep 1 second")

    to_input = '//*[@id="_to"]'
    subject_input = '//*[@id="compose-subject"]'
    composebody_input = '//*[@id="composebody"]'
    send_message_submit = '//*[@id="rcmbtn107"]'
    resend_message_submit = '/html/body/div[8]/div[3]/div/button[1]'

    driver.find_element_by_xpath(to_input).send_keys(to_)
    driver.find_element_by_xpath(subject_input).send_keys(subject_)
    driver.find_element_by_xpath(composebody_input).send_keys(composebody_)

    time.sleep(1)
    driver.find_element_by_xpath(send_message_submit).click()
    time.sleep(1)
    try:
        driver.find_element_by_xpath(resend_message_submit).click()
        time.sleep(3)
    except NoSuchElementException:
        print("NoSuchElementException.")

    driver.quit()
    print("quit.")

def main():
    # [START sheets_get_values]
    sheet = initializeSheets()
    values = readSheets(sheet)
    #description = readSheetsDescription(sheet)
    #senderEmail = readSheetSenderEmail(sheet)

    print('{0} rows retrieved.'.format(len(values)))
    #print('{0} rows retrieved.'.format(len(description)))
    #print('{0} rows retrieved.'.format(len(senderEmail)))
    # [END sheets_get_values]

    #print("Subject: %s" % values)

    if not values:
        print('No data found.')
        return
    else:
        for item, row in enumerate(values, start=1):
            if not row:
                print("List is empty")
                searchDomain_.append(row)
            else:
                searchDomain_.append(row[0])
                #print("Subject: %s" % row)
                print(item, row[3]) #row[0]--> Subject;; row[1]--> composebody;; row[3]--> sender_to_
                if row[3].find("Not Found,,") != -1:
                    print("ignore")
                elif row[3].find("Error,Error,") != -1:
                    print("ignore")
                else :
                    result = [x.strip() for x in row[3].split(',')]
                    for e in result:
                        #print()
                        if valid_email(e):
                            result.remove(e) # here
                    print(''.join(result))
                    #openChromeDriver(row[3], row[0], row[1])
                    #print(result)




if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
