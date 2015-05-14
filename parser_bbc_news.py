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

prefix_url = 'http://www.bbc.com/news/'
main_url = 'http://www.bbc.com'
# http://www.pcworld.com/ajaxGetMoreCategory?start=20&ajaxSearchType=1&catId=3025
# 2206 : Security
# 2119 : Phone
# 2163 : Tables
# 3019 :
# class_="excerpt-text" -> a(href="link")

category_ids = ['world', 'world/africa', 'world/australia', 'world/europe', 'world/latin_america','world/middle_east', 'world/us_and_canada']

for category in category_ids:
	
	print(category)
	
	# Lay noi dung tu url
	response = requests.get(prefix_url + category)
	#print(response.url)

	if response.status_code != 200:
		break

	# Xu ly html
	category_soup = BeautifulSoup(response.content)

	# Lay duong dan cac bai viet
	for a in category_soup.find_all('a', class_="title-link"):
		#print(div.a['href'])
		print(a['href'])

		article_link = a['href']

		if "sport"  in article_link: continue

		if "www." not in article_link:
			article_link = main_url + article_link

		article_page = requests.get(article_link)
		article_soup = BeautifulSoup(article_page.content)
		try:
			title = ' '.join(word for word in word_re.findall(article_soup.find('h1', attrs={"class": "story-body__h1"}).text))
			print(title)
		except Exception as e:
			print(str(e))
			#print(article_link)
			continue
		page_content = ''

		for div in article_soup.find_all('div', class_='story-body__inner'):
			for paragraph in div.find_all('p'):
				if paragraph.string:
					for word in word_re.findall(paragraph.string):
						page_content += word + ' '
					page_content += '\n'

		if page_content:
			path = os.path.join('.', category, category + ' - ' + title + '.txt')

			if not os.path.exists(os.path.dirname(path)):
				os.makedirs(os.path.dirname(path))
			try:
				with open(path, mode='w', encoding='utf8') as corpus_file:
					corpus_file.write(page_content)
			except OSError:
				continue