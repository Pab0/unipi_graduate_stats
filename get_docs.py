#!/usr/bin/env python3
# Invocation: ./get_docs.py
# Usage: Downloads all documents from all articles appearing in the search result of $URL

import os
import requests
from bs4 import BeautifulSoup
import re

URL = 'http://www.cs.unipi.gr/index.php?searchword=ορκωμοσία&ordering=newest&searchphrase=all&limit=0&option=com_search&lang=el'

# Getting links to search results
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
html = list(soup.children)[2]

results = soup.find_all('dt', class_='result-title')

links = [result.a['href'] for result in results]
base_URL = "http://www.cs.unipi.gr"
links = [base_URL + link for link in links]

# Downloading the documents
for link in links:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = list(soup.children)[2]
    file_title = re.search('item&id=(.*)&Itemid=', link).group(1)
    print(link)

    try:
        file_div = soup.find('div', class_='itemFullText')
        file_link = file_div.p.a['href']
        #file_title = re.sub('.*/','',file_link)
        file_link = base_URL + '/' + file_link
    except (AttributeError, TypeError) as e:
        try:
            file_div = soup.find('div', class_='itemAttachmentsBlock')
            file_link = file_div.ul.li.a['href']
            #file_title = file_div.ul.li.a['title']
            file_link = base_URL + '/' + file_link
        except (AttributeError, TypeError) as e:
            try:
                file_link = soup.find('a', target='_blank')['href']
                #file_title = re.sub('.*/','',file_link)
                file_link = base_URL + '/' + file_link
            except (AttributeError, TypeError) as e:
                print("Error getting the file")
    print(file_title) 


    # Storing the documents
    response = requests.get(file_link)
    file_dir = "announcements/"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


    with open(file_dir + file_title, 'wb') as f:
        f.write(response.content)


#print(links)
