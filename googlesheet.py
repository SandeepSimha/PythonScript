import requests
import json
import pandas as pd
from pprint import pprint
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
import pygsheets


#https://docs.google.com/spreadsheets/d/1Gyw5THssc8FqCSqXqni8FHp1_pLjmMHDa6m3Ba501Yk/edit?usp=sharing
#https://docs.google.com/spreadsheets/d/1Gyw5THssc8FqCSqXqni8FHp1_pLjmMHDa6m3Ba501Yk/edit?ts=5f58d7a9#gid=555434050
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1EaSqU0HgAykgIr1se49t6_xwaHoA3kB8ex84781h-io'
#SAMPLE_SPREADSHEET_ID_input = '1Gyw5THssc8FqCSqXqni8FHp1_pLjmMHDa6m3Ba501Yk'
#range A1:AA500 = first 1 - 500 rows of A col
#IF you want A column of 100 to 500 then A100:AA500
SAMPLE_RANGE_NAME = 'Sheet25!A1:AA1000'
countries = []

def fetch(session, domainURL):
    headers = {"Authorization": "Bearer sk_430810a3f52f5f2282da50b515265cc7"}
    with session.get(domainURL, headers=headers,) as response:
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        if response.status_code != 200:
            return "null"


def main():

    global values_input, service
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    # [START sheets_get_values]
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])
    pprint('{0} rows retrieved.'.format(len(values_input)))
    # [END sheets_get_values]

    if not values_input and not values_expansion:
        print('No data found.')
    else:
        #print(values_input)
        for row in values_input:
            # Print columns A only, which correspond to indices 0 and 4.
            #Be carefulll wit this logic
            #print(row)
            #print(str(row[0]))
            #countries.append('https://prospector.clearbit.com/v1/people/search?domain='+str(row))

            if(row[0] != ""):
                countries.append('https://prospector.clearbit.com/v1/people/search?domain='+row[0])
    #sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID_input, range=SAMPLE_RANGE_NAME, valueInputOption=value_input_option, body=[]])

    with requests.Session() as session:
        print("{0:<30} {1:>20}".format("File", "total", "Completed at"))

    #print(countries)
    # The A1 notation of the values to update.
    range_ = 'my-Sheet26!A1:AA500'  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    value_input_option = 'RAW'  # TODO: Update placeholder value.

    value_range_body = {
        # TODO: Add desired entries to the request body. All existing entries
        # will be replaced.
        'values': [1]
    }
    for country in countries:
        if(fetch(session, country) == "null"):
            #raise ValueError('over_quota.')
            request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID_input, range=range_, valueInputOption=value_input_option, body=value_range_body)
            response = request.execute()
            pprint(response)
            #print("over_quota")
        else:
              my_data = fetch(session, country)
              if(my_data['total'] == 0):
                  print ("NULL")
              else:
                  for key in my_data['results']:
                      #print(key['email'], end=", ")
                      #sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID_input, range='Sheet26!A1:AA500', valueInputOption=value_input_option, body=[]])
                      request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID_input, range=range_, valueInputOption={1}, body=value_range_body)
                      response = request.execute()
                      pprint(response)

                  print()

main()
