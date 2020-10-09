import easygui
import os
import csv
from datetime import datetime
import concurrent.futures
import grab_fg_info
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 


filename = easygui.fileopenbox(msg='Select google analytics csv')
# use below for testing
# filename = 'outputs/Analytics Frontier Group Exclude Internal Traffic Pages 20200701-20200731 (2).csvAnalytics Frontier Group Exclude Internal Traffic Pages 20200701-20200731 (2).csv'


fieldnames = ['Page', 'Pageviews', 'UniquePageviews', 'AvgTime', 'Entrances', 'BounceRate', 'PercentExit', 'PageValue']

with open(filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames = fieldnames)
    pages = list(reader)

blogs = []
reports = []

# get blog info
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for page in pages:
        if len(futures) >= 10:
            break
        if '/blogs/' in page['Page']:
            futures.append(executor.submit(grab_fg_info.parse_blog, page))
            print(page['Page'] + ' added')
    for future in concurrent.futures.as_completed(futures):
        blogs.append(future.result())

# get report info
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for page in pages:
        if len(futures) >= 10:
            break
        if '/reports/' in page['Page']:
            futures.append(executor.submit(grab_fg_info.parse_report, page))
            print(page['Page'] + ' added')
    for future in concurrent.futures.as_completed(futures):
        reports.append(future.result())
    
# sort blogs and reports from most to least pageviews
blogs.sort(key=lambda item: locale.atoi(item[0]), reverse=True)
reports.sort(key=lambda item: locale.atoi(item[0]), reverse=True)

# get date for printing at top of page
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

timestamp = datetime.today().strftime('%Y%m%d%H%M')
output = os.path.join('outputs', f'top_pages_{timestamp}.txt')
with open(output, 'w') as textfile:
    textfile.write(page_str)

os.startfile(output)
