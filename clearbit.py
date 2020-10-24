import requests
import json
import time
from multiprocessing import Process
import concurrent.futures
import urllib.request

Domains = ['fritidvildmark.se',
'stadiumsportscamp.se',
'alpingaraget.se',
'bokatennis.nu',
'bonnierbroadcasting.com',
'kt.se']

countries = []

for domain in Domains:
    countries.append('https://prospector.clearbit.com/v1/people/search?domain='+domain)

headers = {"Authorization": "Bearer sk_bb348ca304f4c35bf55d4f3485e94052"}

def load_url(url, timeout):
    return requests.get(url, headers=headers, timeout=timeout)
    #return urllib.request.urlopen(url,timeout=timeout).read()

with concurrent.futures.ThreadPoolExecutor(max_workers=240) as executor:
    future_to_url = dict((executor.submit(load_url, url, 60), url) for url in countries)


    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        if future.exception() is not None:
            print('%r generated an exception: %s' % (url,future.exception()))
        else:
            if(future.result().ok):
                jData = json.loads(future.result().content)

                print(jData['total'])
                #for key in jData['results']:
                #    print(key['email'])
            else:
              # If response code is not ok (200), print the resulting http error code with description
                future.result().raise_for_status()
            #print(future.result().ok)
            #print('%r page is bytes' % (url))
            #print('%r page is %d bytes' % (url, len(future.result())))




url = 'https://prospector.clearbit.com/v1/people/search'
headers = {"Authorization": "Bearer sk_bb348ca304f4c35bf55d4f3485e94052"}
params = dict()
params["domain"] = "kit.se" #bonnierbroadcasting.com
#params["url"] = "https://prospector.clearbit.com/v1/people/search"

# call get service with headers and params
response = requests.get(url, params=params, headers=headers)
#print (response.status_code)
#print ("******************")
#print ("headers:"+ str(response.headers))
#print ("******************")
#print ("response:"+ str(response))

# For successful API call, response code will be 200 (OK)
#if(response.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
#    jData = json.loads(response.content)

#    for key in jData['results']:
        #print(key['email'])
#else:
  # If response code is not ok (200), print the resulting http error code with description
    #response.raise_for_status()
