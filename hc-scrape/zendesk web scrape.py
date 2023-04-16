# Copyright (c) 2023, Neos Wave
# All rights reserved.
# Written by David Jacobs

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
from datetime import datetime
import pytz

time_start = datetime.now(pytz.timezone('America/New_York'))

hc_url = 'https://help.theblacktux.com/hc/en-us'
prefix_articles = 'https://help.theblacktux.com'

client = 'The Black Tux'

s = Service([CHROME DRIVER FILEPATH])


def load_page_sleep(site_sel, secs):
    c = webdriver.ChromeOptions()
    c.add_argument("--incognito")
    driver = webdriver.Chrome(service=s, options=c)
    driver.get(site_sel)
    time.sleep(secs)
    page_html = driver.page_source
    soup = BeautifulSoup(page_html, "html.parser")
    driver.close()
    return soup


collections = load_page_sleep(hc_url, 1)

collection_sections_tags = collections.find_all(attrs= {'class': 'lt-section-link'})

collection_links = []

for a in collection_sections_tags:
    just_collection_link = a['href']
    collection_links.append(prefix_articles + just_collection_link)

print('finished a')

article_pages = []

for cat in collection_links:
    print(cat, f'{collection_links.index(cat) + 1} : {len(collection_links)}')
    category_page = load_page_sleep(cat, 1)
    article_tags = category_page.find_all(attrs= {'class':'lt-article-list-item__link'})
    for tag in article_tags:
        URL = tag['href']
        article_pages.append(prefix_articles + URL)

print('finished b')

breadcrumbs = []
article_title = []
article_text = []

for link in article_pages:
    # help centers can have hundreds of articles so this is to see the progress of running
    print(link, f'{article_pages.index(link) + 1} : {len(article_pages)}')
    article = load_page_sleep(link, 1)
    breadcrumb_trail_tags = article.find_all('ol', 'breadcrumbs')
    for breadcrumb in breadcrumb_trail_tags[:3]:
        breadcrumbs.append(breadcrumb.get_text('|', strip=True))
    article_headlines_tags = article.find('h1', 'lt-article__title lt-mb-4 lt-fs-3 lt-fs-md-1')
    article_title.append(article_headlines_tags.get_text(strip=True))
    article_text_tags = article.find('div', 'lt-article__body')
    article_text.append(article_text_tags.get_text(' ', strip=True))

d = {"Breadcrumbs": breadcrumbs, "Article Title": article_title, "Article Text": article_text}

df = pd.DataFrame.from_dict(d)

df.to_csv(f'{client} KB Scrape.csv', index=False, encoding = 'utf-8-sig')

time_end = datetime.now(pytz.timezone('America/New_York'))

print(f'Started: {time_start}')
print(f'Finished: {time_end}')

try:
    print(time_end - time_start)
except:
    print('din\'t work')
