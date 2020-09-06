import easygui
import os
import requests
import csv
from bs4 import BeautifulSoup
import dateutil.parser
from datetime import datetime

filename = easygui.fileopenbox(msg='Select google analytics csv')

fieldnames = ['Page', 'Pageviews', 'UniquePageviews', 'AvgTime', 'Entrances', 'BounceRate', 'PercentExit', 'PageValue']

with open(filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames = fieldnames)
    pages = list(reader)

blogs = []
reports = []

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

for page in pages:
    if len(blogs) >= 10:
        break
    if '/blogs/' in page['Page']:
        blogs.append(parse_blog(page))
        print(page['Page'] + ' added')

for page in pages:
    if len(reports) >= 10:
        break
    if '/reports/' in page['Page']:
        reports.append(parse_report(page))
        print(page['Page'] + ' added')

date = datetime.strptime(pages[3]['Page'][2:10], '%Y%m%d')
date_str = date.strftime('%B %Y')

page_str = ''

page_str += f'Top blogs for {date_str}:\n'
page_str += '\t'.join(['Views', 'Author', 'Date', 'Title']) + '\n'

for blog in blogs:
    page_str += '\t'.join(blog) + '\n'

page_str += f'\nTop reports for {date_str}:\n'
page_str += '\t'.join(['Views', 'Author', 'Date', 'Title']) + '\n'

for report in reports:
    page_str += '\t'.join(report) + '\n'

with open('top_pages.txt', 'w') as textfile:
    textfile.write(page_str)

os.startfile('top_pages.txt')
