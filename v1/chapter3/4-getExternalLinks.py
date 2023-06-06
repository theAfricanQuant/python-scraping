from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

#Retrieves a list of all Internal links found on a page
def getInternalLinks(bsObj, includeUrl):
    includeUrl = f"{urlparse(includeUrl).scheme}://{urlparse(includeUrl).netloc}"
    internalLinks = []
    #Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href=re.compile(f"^(/|.*{includeUrl})")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks
            
#Retrieves a list of all external links found on a page
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    #Finds all links that start with "http" or "www" that do
    #not contain the current URL
    for link in bsObj.findAll("a", href=re.compile(f"^(http|www)((?!{excludeUrl}).)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html, "html.parser")
    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
    if len(externalLinks) != 0:
        return externalLinks[random.randint(0, len(externalLinks)-1)]
    print("No external links, looking around the site for one")
    domain = f"{urlparse(startingPage).scheme}://{urlparse(startingPage).netloc}"
    internalLinks = getInternalLinks(bsObj, domain)
    return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    
def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print(f"Random external link is: {externalLink}")
    followExternalOnly(externalLink)

followExternalOnly("http://oreilly.com")


