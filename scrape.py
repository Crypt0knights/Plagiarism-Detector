from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import json
from scripts import search




def simple_get(url):
        try:
                with closing(get(url, stream = True)) as response:
                        if is_good_response(response):
                                return  response.content
                        else:
                                return None
        except RequestException as e:
                log_error('Error during requests to {0} : {1}'.format(url, str(e)))
                return None

def is_good_response(response):
        content_type = response.headers['Content-Type'].lower()
        return (response.status_code == 200
                and content_type is not None
                and content_type.find('html') > -1)

def log_error(e):
        print(e)



def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text = True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def scrape_text():
        fd = open('url_percent.json','r')
        data = json.load(fd)
        print(data)
        for urls in data.values():
                print(urls)
                html = urllib.request.urlopen(urls).read()
                f = open("scraped.txt", "w")
                path_scraped = './scraped.txt'
                f.write(text_from_html(html).upper())
                f.close()
                path_source = './check/files/search.txt'
                search.ss(path_source, path_scraped)
                print("Done")

if __name__ == '__main__':
    scrape_text()
