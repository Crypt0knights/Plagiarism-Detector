from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import json
import http.client
import PyPDF2



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

    x  = url.find('.pdf')

    if x != -1:
        print('I found a pdf')
        print('Downloading it ....')
        urllib.request.urlretrieve(url, 'pdf_file.pdf')
        print('Converting pdf to text')
        pdf = PyPDF2.PdfFileReader(open('pdf_file.pdf','rb'))
        text = ''
        for page in pdf.pages:
            text = text + page.extractText()

        fd = open('source{}.txt'.format(i),'w')
        fd.write(text)
        fd.close()
        print('Conversion done')


    else:
        try:
            print('Scraping text from web')
            html = urllib.request.urlopen(url).read()
            # print(text_from_html(html))
            f = open("source{}.txt".format(i),"w")
            text = text_from_html(html)[1:1999]
            f.write(" ".join(text.strip().split()))
            print('scraping done')
            i=i+1
        except urllib.error.HTTPError:
            print("scraping not allowed")
        except urllib.error.URLError:
            print('Certificates verification failed')
        except http.client.IncompleteRead:
            print("Incomplete read scraping not allowed")
