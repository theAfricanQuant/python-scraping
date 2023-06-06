from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password=None, db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE wikipedia")

def getUrl(pageId):
    cur.execute("SELECT url FROM pages WHERE id = %s", (int(pageId)))
    return None if cur.rowcount == 0 else cur.fetchone()[0]

def getLinks(fromPageId):
    cur.execute("SELECT toPageId FROM links WHERE fromPageId = %s", (int(fromPageId)))
    return None if cur.rowcount == 0 else [x[0] for x in cur.fetchall()]

def searchBreadth(targetPageId, currentPageId, depth, nodes):
    if nodes is None or len(nodes) == 0:
        return None
    if depth <= 0:
        return next(([node] for node in nodes if node == targetPageId), None)
    #depth is greater than 0 -- go deeper!
    for node in nodes:
        found = searchBreadth(targetPageId, node, depth-1, getLinks(node))
        if found is not None:
            return found.append(currentPageId)
    return None

nodes = getLinks(1)
targetPageId = 123428
for i in range(0,4):
    found = searchBreadth(targetPageId, 1, i, nodes)
    if found is not None:
        print(found)
        for node in found:
            print(getUrl(node))
        break
    else:
        print("No path found")

