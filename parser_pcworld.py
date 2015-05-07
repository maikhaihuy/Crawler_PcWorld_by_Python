# -*- coding: utf-8 -*-
# Python code to parse news content from VnExpress RSS Feeds.
import os
import re
import traceback
from bs4 import BeautifulSoup   # external lib
import requests                 # external lib
import feedparser               # external lib


MAX_LINKS = 100


word_re = re.compile('(\w+)', flags=re.UNICODE)

parsed_rss = []
parsed_links = []

stop = False

ajax_url = 'http://www.pcworld.com/ajaxGetMoreCategory'
main_url = 'http://www.pcworld.com'
# http://www.pcworld.com/ajaxGetMoreCategory?start=20&ajaxSearchType=1&catId=3025
category_ids = ['2206','3025', '2163', '2119', '3019']

for category in category_ids:
	
	print(category)
	start = 0

	count = 0

	params = {
		'catId': category,
		'start': start,
		'ajaxSearchType': 1
	}

	while True:

		params['start'] = start
		# Lay noi dung tu url
		response = requests.get(ajax_url, params=params)
		print(response.url)
		print(response)
		if response.status_code != 200:
			break

		# Xu ly html
		category_soup = BeautifulSoup(response.content)

		# Lay duong dan cac bai viet
		for div in category_soup.find_all('div', class_="excerpt-text"):
			print(div.a['href'])

			article_link = div.a['href']
			article_page = requests.get(main_url + article_link)
			article_soup = BeautifulSoup(article_page.content)
			try:
				title = ' '.join(word for word in word_re.findall(article_soup.find('h1', attrs={"itemprop": "name"}).text))
				#print(title)
			except Exception as e:
				#print(str(e))
				#print(article_link)
				continue
			page_content = ''

			for section in article_soup.find_all('section', class_='page'):
				for paragraph in section.find_all('p'):
					if paragraph.string:
						for word in word_re.findall(paragraph.string):
							page_content += word + ' '
						page_content += '\n'

			if page_content:
				count += 1
				path = os.path.join('.', category, category + ' - ' + title + '.txt')

				if not os.path.exists(os.path.dirname(path)):
					os.makedirs(os.path.dirname(path))
				try:
					with open(path, mode='w', encoding='utf8') as corpus_file:
						corpus_file.write(page_content)
				except OSError:
					continue

			if count >= MAX_LINKS:
				break
		if count >= MAX_LINKS:
			break
		start += 10