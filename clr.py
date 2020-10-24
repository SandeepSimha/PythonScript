import requests
from timeit import default_timer
import json
import time
from multiprocessing import Process
import concurrent.futures
import urllib.request
import csv

def fetch(session, domainURL):
    headers = {"Authorization": "Bearer sk_bb348ca304f4c35bf55d4f3485e94052"}
    with session.get(domainURL, headers=headers,) as response:
        data = json.loads(response.content)
        #if response.status_code == 200:
        #    print(data['total'])
        # Return .csv data for future consumption
        return data


with requests.Session() as session:
    print("{0:<30} {1:>20}".format("File", "total", "Completed at"))



Domains = ['fritidvildmark.se',
'stadiumsportscamp.se',
'alpingaraget.se',
'bokatennis.nu',
'bonnierbroadcasting.com',
'kt.se']

countries = []

for domain in Domains:
    countries.append('https://prospector.clearbit.com/v1/people/search?domain='+domain)

total_start_time = default_timer()
for country in countries:
    my_data = fetch(session, country)

    if(my_data['total'] == 0):
        print("NULL")

    else:
        for key in my_data['results']:
            print(key['email'], end=", ")

        print()


    elapsed = default_timer() - total_start_time
    time_completed_at = "{:5.2f}s".format(elapsed)
    #print("{0:<30} {1:>20}".format(csv, my_data['total'], time_completed_at))
