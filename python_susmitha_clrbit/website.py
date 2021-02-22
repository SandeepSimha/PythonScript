from __future__ import print_function

import os
import os.path
import pickle
import re
import time

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1_r4da-8nTEwpOLs64dIksoD9xZEiLCFfucidEf70P8g'  # chsandeep511@gmail.com

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
    # TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    # The A1 notation of the values to update.
    # start with A2 always
    read_range_ = 'Sheet30!A204:AA401'  # Should be same Row number at line 60: Here I am reading at Column 'A' 10th Row to 20th row

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=read_range_).execute()
    values = result.get('values', [])
    return values


def valid_email(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


def composeMessageSend(driver, to_, subject_, composebody_):
    time.sleep(4)
    print("Click Compose Button")
    driver.find_element_by_xpath('//*[@id="rcmbtn107"]').click()
    print("Sleep 2 second %s" %to_)
    time.sleep(2)

    to_input = '//*[@id="_to"]'
    subject_input = '//*[@id="compose-subject"]'
    composed_input = '//*[@id="composebody"]'
    send_message_submit = '//*[@id="rcmbtn107"]'
    resend_message_submit = '/html/body/div[8]/div[3]/div/button[1]'
    resend_message_submit_again = '/html/body/div[9]/div[3]/div/button[1]'
    invalid_email_address =  '/html/body/div[9]/div[2]'

    error_occured_view = '//*[@id="ui-id-19"]'

    driver.find_element_by_xpath(to_input).send_keys(to_)
    driver.find_element_by_xpath(subject_input).send_keys(subject_)
    driver.find_element_by_xpath(composed_input).send_keys(composebody_)
    print("Sleep 1 second")
    time.sleep(1)
    driver.find_element_by_xpath(send_message_submit).click()
    print("Sleep 2 second")
    time.sleep(2)
    try:
        driver.find_element_by_xpath(resend_message_submit).click()
        time.sleep(3)
    except NoSuchElementException:
        print("resend_message_submit NoSuchElementException.")

    try:
        driver.find_element_by_xpath(resend_message_submit_again).click()
        time.sleep(3)
    except NoSuchElementException:
        print("Too Many Public Recipeints.")

    try:
        driver.find_element_by_xpath(invalid_email_address).click()
        print("found invalid_email_address.")
        driver.quit()
    except NoSuchElementException:
        print("invalid_email_address NoSuchElementException.")

    #driver.quit()
    print("quit.")

def openChromeDriver():
    chromedriver = "/Users/sancheru/Downloads/chromedriver"

    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=chrome-data")
    driver = webdriver.Chrome(chromedriver)  # ,options=chrome_options)
    driver.get('https://caprica.seoboxes.com:2096/cpsess8220829249/3rdparty/roundcube/?_task=mail&_action=compose&_id=14557673775fb5a90c1c498')

    username_input = '//*[@id="user"]'
    password_input = '//*[@id="pass"]'
    login_submit = '//*[@id="login_submit"]'

    driver.find_element_by_xpath(username_input).send_keys("mike@viztraffic.com")  # stewardsmike@trafficluxury.com
    driver.find_element_by_xpath(password_input).send_keys("fc24uxdara")
    driver.find_element_by_xpath(login_submit).click()
    #driver.maximize_window()
    #composeMessageSend(driver, to_, subject_, composebody_)
    return driver


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
        driver = openChromeDriver()
        count = 1
        for item, row in enumerate(values, start=1):
            if not row:
                print("List is empty")
                searchDomain_.append(row)
            else:
                searchDomain_.append(row[0])
                #print("Email: %d" % item)
                #print("Row: %s" % row[20]) #row[0]--> Domain;;row[20]--> Email List;;row[22]--> Title;; row[23]--> Description;;
                # print(item, row[3]) #row[0]--> Subject;; row[1]--> composed;; row[2]--> sender_to_
                if row[20].find("Not found") != -1 or row[20].find("Not Found") != -1 or row[20].find("Error") != -1 or row[20].find("error") != -1 or row[20].find("redirected") != -1 or row[20].find("Redirected") != -1 or row[20].find("This site can’t be reached") != -1 or row[20].find("This page isn’t working") != -1 :
                    print("ignore")
                else:
                    #print("Email: %d" % item, row[20], row[22], row[23])
                    #driver, to_, subject_, composebody_
                    #driver, row[20], row[22], row[23]
                    print('{0}'.format(count))
                    count = count + 1
                    composeMessageSend(driver, row[20], row[22], row[23])
                    # print(result)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
