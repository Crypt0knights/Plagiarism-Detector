from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import json
import http.client



url_percent=open('./url_percent.json')
data = json.load(url_percent)



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

i = 1
for url in data.values():
#print(i)
#print(url)
    try:
        html = urllib.request.urlopen(url).read()
        print(text_from_html(html))
        f = open("source{}.txt".format(i),"w")
        text = text_from_html(html)[1:1999]
        f.write(" ".join(text.strip().split()))
    except urllib.error.HTTPError:
        print("scraping not allowed")
    except http.client.IncompleteRead:
        print("Incomplete read scraping not allowed")
    i+=1

