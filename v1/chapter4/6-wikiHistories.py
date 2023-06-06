from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup
import datetime
import json
import random
import re

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen(f"http://en.wikipedia.org{articleUrl}")
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

def getHistoryIPs(pageUrl):
    #Format of revision history pages is: 
    #http://en.wikipedia.org/w/index.php?title=Title_in_URL&action=history
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = (
        f"http://en.wikipedia.org/w/index.php?title={pageUrl}&action=history"
    )
    print(f"history url is: {historyUrl}")
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    #finds only the links with class "mw-anonuserlink" which has IP addresses 
    #instead of usernames
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    return {ipAddress.get_text() for ipAddress in ipAddresses}


def getCountry(ipAddress):
    try:
        response = (
            urlopen(f"http://freegeoip.net/json/{ipAddress}")
            .read()
            .decode('utf-8')
        )
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson["region_name"]
    
links = getLinks("/wiki/Python_(programming_language)")


while (len(links) > 0):
    for link in links:
        print("-------------------")
        historyIPs = getHistoryIPs(link.attrs["href"])
        for historyIP in historyIPs:
            country = getCountry(historyIP)
            if country is not None:
                print(f"{historyIP} is from {country}")

    newLink = links[random.randint(0, len(links)-1)].attrs["href"]
    links = getLinks(newLink)
