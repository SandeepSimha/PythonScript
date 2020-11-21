import re
import requests
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
import operator
from google.colab import files

original_url = input("Enter the website url: ")

unscraped = deque([original_url])

scraped = set()

emails = set()

def findMails(soup):
    for name in soup.find_all('a'):
        if(name is not None):
            emailText=name.text
            print(name)
            match=bool(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',emailText))
            if('@' in emailText and match==True):
                emailText=emailText.replace(" ",'').replace('\r','')
                emailText=emailText.replace('\n','').replace('\t','')
                if(len(mails)==0)or(emailText not in mails):
                    print(emailText)
                mails.append(emailText)

while len(unscraped):
    print(unscraped)
    url = unscraped.popleft()
    scraped.add(url)

    parts = urlsplit(url)

    base_url = "{0.scheme}://{0.netloc}".format(parts)
    if '/' in parts.path:
      path = url[:url.rfind('/')+1]
    else:
      path = url

    print("Crawling URL %s" % url)
    #print("Crawling URL %s" % base_url)

    try:
        print("try")
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        print(requests.exceptions)
        continue

    #  new_emails = set(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+', response.text))
    #print(response.text)
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+", response.text, re.I))
    #new_emails = set(re.findall(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?", response.text, re.I))
    emails.update(new_emails)
    print(new_emails)


    soup = BeautifulSoup(response.text, 'lxml')
    #soup=BeautifulSoup(response.text,'html.parser')
    #findMails(soup)

    #print(soup)

    for anchor in soup.find_all("a"):
      #print(anchor.attrs)
      if "href" in anchor.attrs:
          #print(anchor)
          #print(re.search(r'\w+$', anchor))
          #print(operator.contains(anchor, "kontakt"))
          if(anchor.find("kontakt") == -1):
              anchor.attrs["href"]
              #print(anchor.attrs["href"])

          link = anchor.attrs["href"]
          #print(link)

      else:
        link = ''
        #print(anchor.attrs)
        if link.startswith('/'):
            #print("startswith")
            link = base_url + link

        elif not link.startswith('http'):
            #print("ttp")
            link = path + link

        if not link.endswith(".gz"):
          if not link in unscraped and not link in scraped:
              unscraped.append(link)

#print(emails)
'''df = pd.DataFrame(emails, columns=["Email"])
df.to_csv('email.csv', index=False)

files.download("email.csv")'''
