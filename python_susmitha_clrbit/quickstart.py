from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import json

# If modifying these scopes, delete the file token.pickle.
#https://docs.google.com/spreadsheets/d/1EaSqU0HgAykgIr1se49t6_xwaHoA3kB8ex84781h-io/edit?usp=sharing
# https://docs.google.com/spreadsheets/d/1Gyw5THssc8FqCSqXqni8FHp1_pLjmMHDa6m3Ba501Yk/edit?usp=sharing
# https://docs.google.com/spreadsheets/d/19U9hMr995HcNIUYL0ij8xRn37xz2yZxI_uasQFDizRM/edit?usp=sharing
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1EaSqU0HgAykgIr1se49t6_xwaHoA3kB8ex84781h-io' #sandeep.dev.511@gmail.com
#https://docs.google.com/spreadsheets/d/1T4oTT9aTbau76B9wAcx_t21COgMSM_Cq3_Ec2Mc5cUs
SAMPLE_SPREADSHEET_ID = '1_r4da-8nTEwpOLs64dIksoD9xZEiLCFfucidEf70P8g' #chsandeep511@gmail.com

#https://docs.google.com/spreadsheets/d/1XawJviNBBUJdoMmepxbZKG9Coa0yaVEfDl2xb8TIPEI/edit?usp=sharing
#https://docs.google.com/spreadsheets/d/1_r4da-8nTEwpOLs64dIksoD9xZEiLCFfucidEf70P8g/edit?usp=sharing

searchDomain_ = []
overQuota = []

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


def updateToSheets(sheet):

    #TODO:// Update with your Sheet number and from `where to where` you want to read the domian list: Susmitha
    range_ = 'Sheet31!R2:AA401' #Should be same Row number at line 50: Here I am updating at Column 'J' 10th Row to 20th row

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
    #print(response)


def fetch(session, domainURL):

    #TODO://update Token when you get Over_quota: Susmitha
    headers = {"Authorization": "Bearer sk_d65f6e634493e0ea8a7b14e300a381f3"}
    with session.get(domainURL, headers=headers,) as response:
        if response.status_code == 200:
            data = json.loads(response.content)
            return data
        if response.status_code == 402:
            print(response.status_code)
            return "null"
        if response.status_code != 200:
            print(response.status_code)
            #return "null"


def main():
    # [START sheets_get_values]
    sheet = initializeSheets()
    values = readSheets(sheet)
    print('{0} rows retrieved.'.format(len(values)))
    print('{0} వరుసలు తీసుకుంది.'.format(len(values)))
    # [END sheets_get_values]

    if not values:
        print('No data found.')
        return
    else:

        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            #print('%s, %s' % (row[0], row[1]))
            #print(row[0])
            searchDomain_.append('https://prospector.clearbit.com/v1/people/search?domain='+row[0])


    with requests.Session() as session:
        print("{0:<30} {1:>20}".format("", "", ""))
        print("*********************************************************************************************************")



    for domain in searchDomain_:
        my_data = fetch(session, domain)
        if(my_data== "null"):
            print("కోటాను మించిపోయింది, దయచేసి బేరర్ టోకెన్‌ను లైన్ 85వ సంఖ్య  వద్ద సవరించండి")
            break
            #raise ValueError('over_quota.')

        else:
              if(str(my_data) == 'None'):
                  print ("Sandeep")
                  overQuota.append("NULL")
                  print ("NULL")
              elif(my_data['total'] == 0):
                overQuota.append("NULL")
                print ("NULL")
              else:
                emailList = []
                for key in my_data['results']:
                    print(key['email'], end=", ")
                    emailList.append(key['email'])
                print("")
                overQuota.append(str(emailList))

    print(overQuota)
    updateToSheets(sheet)
    #If you get HttpError 400/403  or other error codes then Share your Sheets  to "Anyone on the internet with this link can edit"


if __name__ == '__main__':
    main()
