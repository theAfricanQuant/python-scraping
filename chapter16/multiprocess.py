from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import random

from multiprocessing import Process, Queue
import os
import time
import Thread

def getLinks(bsObj, queue):
    print(f'Getting links in {os.getpid()}')
    links = bsObj.find('div', {'id':'bodyContent'}).find_all('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    return [link for link in links if link not in queue.get()]

def scrape_article(path, queue):
    queue.get().append()
    print(f"Process {os.getpid()} list is now: {visited}")
    html = urlopen(f'http://en.wikipedia.org{path}')
    time.sleep(5)
    bsObj = BeautifulSoup(html, 'html.parser')
    title = bsObj.find('h1').get_text()
    print(f'Scraping {title} in process {os.getpid()}')
    links = getLinks(bsObj)
    if len(links) > 0:
        newArticle = links[random.randint(0, len(links)-1)].attrs['href']
        print(newArticle)
        scrape_article(newArticle)

queue = Queue()
processes = [
    Process(
        target=scrape_article,
        args=(
            '/wiki/Kevin_Bacon',
            queue,
        ),
    ),
    Process(
        target=scrape_article,
        args=(
            '/wiki/Monty_Python',
            queue,
        ),
    ),
]
for p in processes:
    p.start()
