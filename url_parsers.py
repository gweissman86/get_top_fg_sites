import requests
from bs4 import BeautifulSoup
import dateutil

def parse_blog(blog_url):
    try:
        url = r'https://frontiergroup.org' + blog_url
        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        title = soup.title.string
        title = title[0:title.find(' |')]
        print(title)
        byline = soup.find(class_ = 'blog-byline').getText()
        byline = byline[3:byline.find(',')]
        print(byline)
        rawdate = soup.find(class_ = 'date-display-single').get('content')
        dateobj = dateutil.parser.parse(rawdate)
        datestring = dateobj.strftime(r"%m/%d/%Y")
        print(datestring)
        return [byline, datestring, title]
    except:
        return ['ERROR', 'ERROR', 'ERROR']
