from bs4 import BeautifulSoup
import dateutil.parser
import requests

def parse_report(page):
    try:
        url = r'https://frontiergroup.org' + page['Page']
        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.title.string
        title = title[0:title.find(' |')]
        byline_class = 'field field-name-field-report-byline field-type-text-long field-label-above'
        byline = soup.find(class_ = byline_class).getText()
        byline = byline[len('Written by: '):-1]
        rawdate = soup.find(class_ = 'date-display-single').get('content')
        dateobj = dateutil.parser.parse(rawdate)
        datestring = dateobj.strftime(r"%m/%d/%Y")
        return [page['Pageviews'], byline, datestring, title]
    except:
        return [page['Pageviews'], page['Page'], 'ERR', 'ERR']

def parse_blog(page):
    try:
        url = r'https://frontiergroup.org' + page['Page']
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.title.string
        title = title[0:title.find(' |')]
        byline = soup.find(class_ = 'blog-byline').getText()
        byline = byline[3:byline.find(',')]
        rawdate = soup.find(class_ = 'date-display-single').get('content')
        dateobj = dateutil.parser.parse(rawdate)
        datestring = dateobj.strftime(r"%m/%d/%Y")
        return [page['Pageviews'], byline, datestring, title]
    except:
        return [page['Pageviews'], page['Page'], 'ERR', 'ERR']
